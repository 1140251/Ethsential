import os
from time import time
from datetime import timedelta
import docker
from joblib import Parallel, delayed
from solidity_parser import parser
client = docker.from_env()
SOLIDITY_DEFAULT_VERSION = "0.6.4"


def mount_volumes(dir_path):
    try:

        volume_bindings = {os.path.abspath(
            dir_path): {'bind': '/analysis', 'mode': 'rw'}}
        return volume_bindings
    except os.error as err:
        print(err)


def start_container(filePath, lang_version, volume_bindings, tool):
    container = None
    start = time()
    try:
        cmd = tool.command.format(contract='/analysis/' + os.path.basename(filePath).replace(
            '\\', '/'), version=lang_version)
        container = client.containers.run(tool.image,
                                          cmd,
                                          detach=True,
                                          volumes=volume_bindings)

        container.wait(timeout=(30 * 80))
        output = container.logs().decode('utf8').strip()
        result = tool.parse(output)
        result["duration"] = str(timedelta(seconds=round(time() - start)))
        return result
    except Exception as exception:
        return {"success": False, "exception": str(exception), "duration": str(timedelta(seconds=round(time() - start)))}
    finally:
        stop_container(container)
        remove_container(container)


def stop_container(container):
    try:
        if container is not None:
            container.stop(timeout=0)
    except (docker.errors.APIError) as err:
        print(err)


def remove_container(container):
    try:
        if container is not None:
            container.remove()
    except (docker.errors.APIError) as err:
        print(err)


def analyse_file(filePath, lang, tools):
    volume_bindings = mount_volumes(os.path.dirname(filePath))
    lang_version = get_lang_version(filePath, lang)

    results = []

    results = Parallel(n_jobs=1)(delayed(start_container)(
        filePath, lang_version, volume_bindings, tool) for tool in tools)
    # results.append(result)
    return results


def get_lang_version(file, lang):
    if lang == 'solidity':
        try:
            with open(file, 'r', encoding='utf-8') as fd:
                source_unit = parser.parse(fd.read())
                source_unit_object = parser.objectify(source_unit)
                pragmas = source_unit_object.pragmas
                solc_version = pragmas[0]['value']
                solc_version = solc_version.strip('^')
                return solc_version
        except Exception as exception:
            print(exception)
            pass
        return SOLIDITY_DEFAULT_VERSION
    else:
        return ''


def install_tools(tools):
    for tool in tools:
        try:
            client.images.pull(tool.image)
        except (docker.errors.APIError, docker.errors.BuildError, Exception) as error:
            if hasattr(error, 'explanation'):
                raise error
            else:
                raise ValueError('Docker not found')
