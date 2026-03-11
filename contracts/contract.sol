// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProductRegistry {

    struct Product {
        uint id;
        string name;
        string ingredients;
        string allergens;
        string nutrition;
        address manufacturer;
        uint timestamp;
    }

    uint public productCount = 0;
    mapping(uint => Product) public products;

    function addProduct(
        string memory _name,
        string memory _ingredients,
        string memory _allergens,
        string memory _nutrition
    ) public {

        productCount++;

        products[productCount] = Product(
            productCount,
            _name,
            _ingredients,
            _allergens,
            _nutrition,
            msg.sender,
            block.timestamp
        );
    }

    function getProduct(uint _id) public view returns (
        uint,
        string memory,
        string memory,
        string memory,
        string memory,
        address,
        uint
    ) {
        Product memory p = products[_id];
        return (
            p.id,
            p.name,
            p.ingredients,
            p.allergens,
            p.nutrition,
            p.manufacturer,
            p.timestamp
        );
    }
}
