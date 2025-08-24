// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * Minimal ETH forwarder. Any ETH sent is auto-forwarded to payout.
 */
contract ETHForwarder {
    address public immutable payout;

    event Forwarded(address indexed from, uint256 amount, address indexed to);

    constructor(address _payout) {
        require(_payout != address(0), "payout=0");
        payout = _payout;
    }

    receive() external payable {
        (bool ok, ) = payable(payout).call{value: msg.value}("");
        require(ok, "forward failed");
        emit Forwarded(msg.sender, msg.value, payout);
    }

    // in case someone sends ETH with data and no receive()
    fallback() external payable {
        if (msg.value > 0) {
            (bool ok, ) = payable(payout).call{value: msg.value}("");
            require(ok, "forward failed");
            emit Forwarded(msg.sender, msg.value, payout);
        }
    }
}
