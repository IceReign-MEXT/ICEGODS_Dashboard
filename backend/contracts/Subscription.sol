// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Subscription {
    address public owner;
    uint256 public constant PRICE = 0.01 ether;

    mapping(address => bool) public subscribers;

    event Subscribed(address indexed user, uint256 amount);

    constructor(address _owner) {
        owner = _owner;
    }

    function subscribe() external payable {
        require(msg.value == PRICE, "Incorrect amount");
        subscribers[msg.sender] = true;
        payable(owner).transfer(msg.value);
        emit Subscribed(msg.sender, msg.value);
    }

    function isSubscribed(address user) external view returns (bool) {
        return subscribers[user];
    }
}
