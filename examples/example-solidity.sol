pragma solidity 0.5.10;

contract EthTxOrderDependenceMinimal {
    address payable public  owner;
    bool public claimed;
    uint public reward;

    constructor() public {
        owner = msg.sender;
    }

    function setReward() public payable {
        require (!claimed);

        require(msg.sender == owner);
        owner.transfer(reward);
        reward = msg.value;
    }

    function claimReward(uint256 submission) public{
        require (!claimed);
        require(submission < 10);

        msg.sender.transfer(reward);
        claimed = true;
    }
}