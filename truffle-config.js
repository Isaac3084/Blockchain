const HDWalletProvider = require('@truffle/hdwallet-provider');
const mnemonic = "inflict broken ankle swift rookie nice dilemma sadness use name device wish";

module.exports = {
  networks: {
    sepolia: {  // Using Sepolia testnet
      provider: () => new HDWalletProvider(
        mnemonic, 
        `https://sepolia.infura.io/v3/068c53b2d79c4b58bd4d45b002e81372`
      ),
      network_id: 11155111,  // Sepolia's network id
      gas: 5500000,
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: true
    },
  },
  compilers: {
    solc: {
      version: "0.8.11",
    }
  }
}; 