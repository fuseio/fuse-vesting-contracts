const { ethers, network } = require('hardhat')
const { expect } = require('chai')

const { advanceTimeAndBlock } = require('./utilities/time')

const DAY_IN_SECONDS = 86400

describe('VestingVault13', () => {
    let vestingVault
    let token
    let signers

    beforeEach(async () => {
        signers = await ethers.getSigners()

        const Token = await ethers.getContractFactory('ERC20Mock')
        token = await Token.deploy('VestToken', 'VT', "1000")
        await token.deployed()
        
        const VestingVault13 = await ethers.getContractFactory('VestingVault13')
        vestingVault = await VestingVault13.deploy(token.address)
        await vestingVault.deployed()
    })

    describe('addTokenGrant', () => {
        beforeEach(async () => {
            await token.approve(vestingVault.address, "1000")
        })

        it('should fail if vestingCliff is more than 10 years', async () => { 
            await expect(
                vestingVault.addTokenGrant(
                    signers[1].address,
                    0,
                    "1000",
                    365 * 11,
                    366 * 11
                )
            ).to.be.revertedWith('more than 10 years')
        })

        it('should fail if vestingDuration is more than 25 years', async () => { 
            await expect(
                vestingVault.addTokenGrant(
                    signers[1].address,
                    0,
                    "1000",
                    365 * 26,
                    0
                )
            ).to.be.revertedWith('more than 25 years')
        })

        it('should fail if vestingDuration < vestingCliff', async () => {
            await expect(
                vestingVault.addTokenGrant(
                    signers[1].address,
                    0,
                    "1000",
                    5,
                    10
                )
            ).to.be.revertedWith('Duration < Cliff')
        })

        it('should fail if vestingDuration is zero', async () => {
            await expect(
                vestingVault.addTokenGrant(
                    signers[1].address,
                    0,
                    0,
                    10,
                    5
                )
            ).to.be.revertedWith('amountVestedPerDay > 0')
        })

        it('should transfer tokens to vault', async () => {
            await vestingVault.addTokenGrant(
                signers[1].address,
                0,
                "1000",
                365,
                30
            )

            expect(await token.balanceOf(vestingVault.address)).to.equal('1000')
        })
    })

    describe('claimVestedTokens', () => {
        beforeEach(async () => {
            await token.approve(vestingVault.address, "1000")
            await vestingVault.addTokenGrant(
                signers[1].address,
                0,
                "1000",
                365,
                0
            )
        })

        it('only recipient can claim their grant', async () => {
            await advanceTimeAndBlock(DAY_IN_SECONDS * 10)

            await expect(
                vestingVault.claimVestedTokens(0)
            ).to.be.revertedWith('not recipient')

            await vestingVault.connect(signers[1]).claimVestedTokens(0)

            expect(await token.balanceOf(signers[1].address)).to.be.equal('20')
        })

        it('recipient can claim their grant daily', async () => {
            await advanceTimeAndBlock(DAY_IN_SECONDS * 10)

            await vestingVault.connect(signers[1]).claimVestedTokens(0)

            expect(await token.balanceOf(signers[1].address)).to.be.equal('20')

            await advanceTimeAndBlock(DAY_IN_SECONDS * 1)

            await vestingVault.connect(signers[1]).claimVestedTokens(0)

            expect(await token.balanceOf(signers[1].address)).to.be.equal('22')
        })
    })
})
