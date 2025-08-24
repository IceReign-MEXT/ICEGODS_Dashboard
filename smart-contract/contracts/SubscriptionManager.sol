// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract SubscriptionManager {
    address public immutable payout;
    address public owner;

    struct Plan {
        uint256 priceWei;
        uint256 durationDays;
    }

    mapping(uint8 => Plan) public plans;
    mapping(address => uint256) public expiresAt;

    event Subscribed(address indexed user, uint8 indexed plan, uint256 amountWei, uint256 newExpiry);
    event PlanUpdated(uint8 indexed plan, uint256 priceWei, uint256 durationDays);
    event OwnerChanged(address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor(address _payout) {
        require(_payout != address(0), "payout=0");
        payout = _payout;
        owner = msg.sender;

        // plan 1: monthly, 0.01 ETH, 30 days
        plans[1] = Plan({priceWei: 10_000_000_000_000_000, durationDays: 30});
        // plan 2: yearly, 0.10 ETH, 365 days
        plans[2] = Plan({priceWei: 100_000_000_000_000_000, durationDays: 365});
        // plan 3: lifetime (100 years as proxy), 0.25 ETH
        plans[3] = Plan({priceWei: 250_000_000_000_000_000, durationDays: 36500});
    }

    function setPlan(uint8 planId, uint256 priceWei, uint256 durationDays) external onlyOwner {
        plans[planId] = Plan(priceWei, durationDays);
        emit PlanUpdated(planId, priceWei, durationDays);
    }

    function setOwner(address newOwner) external onlyOwner {
        require(newOwner != address(0), "owner=0");
        owner = newOwner;
        emit OwnerChanged(newOwner);
    }

    function subscribe(uint8 planId) external payable {
        Plan memory p = plans[planId];
        require(p.priceWei > 0, "plan not set");
        require(msg.value >= p.priceWei, "insufficient payment");

        uint256 prev = expiresAt[msg.sender];
        uint256 base = block.timestamp > prev ? block.timestamp : prev;
        uint256 newExpiry = base + (p.durationDays * 1 days);
        expiresAt[msg.sender] = newExpiry;

        // forward funds to payout wallet
        (bool ok, ) = payout.call{value: msg.value}("");
        require(ok, "payout failed");

        emit Subscribed(msg.sender, planId, msg.value, newExpiry);
    }

    function timeLeft(address user) external view returns (uint256) {
        uint256 exp = expiresAt[user];
        if (exp <= block.timestamp) return 0;
        return exp - block.timestamp;
    }
}
