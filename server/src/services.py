import os
import multiprocessing
import docker
from solidity_parser import parser

client = docker.from_env()
SOLIDITY_DEFAULT_VERSION = "0.6.4"


def mount_volumes(dir_path):
    try:
        volume_bindings = {os.path.abspath(
            dir_path): {'bind': '/' + dir_path.replace(':', ''), 'mode': 'rw'}}
        return volume_bindings
    except os.error as err:
        print(err)


def start_container(filePath, lang, volume_bindings, tool):
    container = None
    try:
        lang_version = get_lang_version(filePath, lang)

        cmd = tool.command.format(contract='/' + filePath.replace(
            '\\', '/'), version=lang_version)
        container = client.containers.run(tool.image,
                                          cmd,
                                          detach=True,
                                          volumes=volume_bindings)

        container.wait(timeout=(30 * 80))
        output = container.logs().decode('utf8').strip()
        return tool.parse(output)
    except Exception as exception:
        return {"sucess": False, "exception": exception}
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
    pool = multiprocessing.Pool()
    results = []
    results = [pool.apply(start_container, args=(
        filePath, lang, volume_bindings, tool)) for tool in tools]
    pool.close()
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
        print('....installing ' + tool.image)
        try:
            client.images.pull(tool.image+':latest')
        except docker.errors.APIError as error:
            return error.explanation
