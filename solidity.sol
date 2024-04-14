pragma solidity ^0.8.0;

contract MLStudio {
    address public owner;
    mapping(address => bool) public authorizedUsers;
    mapping(bytes32 => bytes) private modelParams;

    event ModelParametersStored(bytes32 indexed modelId, bytes params);
    event ModelParametersRetrieved(bytes32 indexed modelId, bytes params);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can call this function");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedUsers[msg.sender], "Sender is not authorized to call this function");
        _;
    }

    function addAuthorizedUser(address _user) external onlyOwner {
        authorizedUsers[_user] = true;
    }

    function removeAuthorizedUser(address _user) external onlyOwner {
        authorizedUsers[_user] = false;
    }

    function storeModelParameters(bytes32 _modelId, bytes memory _params) external onlyAuthorized {
        modelParams[_modelId] = _params;
        emit ModelParametersStored(_modelId, _params);
    }

    function retrieveModelParameters(bytes32 _modelId) external view onlyAuthorized returns (bytes memory) {
        return modelParams[_modelId];
    }
}
 