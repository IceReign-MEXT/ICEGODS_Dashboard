// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Subscription {
    address public payoutWallet;
    mapping(address => uint256) public subscriptions;

    constructor(address _payoutWallet) {
        payoutWallet = _payoutWallet;
    }

    function subscribe() external payable {
        require(msg.value >= 0.01 ether, "Minimum 0.01 ETH");
        subscriptions[msg.sender] = block.timestamp;
        payable(payoutWallet).transfer(msg.value);
    }

    function getSubscription(address _user) external view returns (uint256) {
        return subscriptions[_user];
    }
}
