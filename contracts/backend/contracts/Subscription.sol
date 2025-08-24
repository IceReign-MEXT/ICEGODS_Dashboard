// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Subscription {
    address public owner;
    address public payoutWallet;
    uint256 public monthlyFee = 0.01 ether;

    mapping(address => uint256) public subscriptions;

    event Subscribed(address subscriber, uint256 amount, uint256 timestamp);

    constructor(address _payoutWallet) {
        owner = msg.sender;
        payoutWallet = _payoutWallet;
    }

    function subscribe() external payable {
        require(msg.value == monthlyFee, "Incorrect subscription amount");
        subscriptions[msg.sender] = block.timestamp;
        payable(payoutWallet).transfer(msg.value);
        emit Subscribed(msg.sender, msg.value, block.timestamp);
    }

    function getSubscription(address _user) external view returns (uint256) {
        return subscriptions[_user];
    }
}
