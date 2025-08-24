// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function decimals() external view returns (uint8);
}

contract USDTPayments {
    address public immutable payout;
    IERC20 public immutable usdt;
    uint256 public price; // in USDT base units (USDT = 6 decimals)

    event Subscribed(address indexed user, uint256 amount, address indexed payout);

    constructor(address _usdt, address _payout, uint256 _price) {
        require(_usdt != address(0) && _payout != address(0), "0 addr");
        usdt = IERC20(_usdt);
        payout = _payout;
        price = _price; // e.g., 10 * 1e6 for 10 USDT
    }

    function setPrice(uint256 _price) external {
        // (Optional) lock this or add an owner if you want; left open for simplicity
        price = _price;
    }

    function subscribe(uint256 amount) external {
        require(amount >= price, "amount < price");
        bool ok = usdt.transferFrom(msg.sender, payout, amount);
        require(ok, "USDT transferFrom failed");
        emit Subscribed(msg.sender, amount, payout);
    }
}
