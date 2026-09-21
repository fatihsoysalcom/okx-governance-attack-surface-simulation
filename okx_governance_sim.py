import random

# --- Configuration ---
TOTAL_TOKENS = 1000000
MIN_VOTE_THRESHOLD = 0.05 # 5% of total tokens to propose
QUORUM_THRESHOLD = 0.10   # 10% of total tokens must vote for a proposal to pass
SUCCESS_VOTE_PERCENT = 0.60 # 60% 'yes' votes needed to pass if quorum is met

# --- Mock Data Structures ---
class Proposal:
    def __init__(self, proposal_id, description, proposer_address):
        self.proposal_id = proposal_id
        self.description = description
        self.proposer_address = proposer_address
        self.votes = {'yes': 0, 'no': 0}
        self.voters = set()
        self.is_passed = None

class TokenHolder:
    def __init__(self, address, balance):
        self.address = address
        self.balance = balance

# --- Simulation Logic ---
def simulate_governance_attack_surface():
    print("--- OKX Governance Attack Surface Simulation ---")

    # 1. Initialize token holders (simulating users and whales)
    token_holders = [
        TokenHolder("user_001", 10000),
        TokenHolder("user_002", 5000),
        TokenHolder("whale_001", 500000), # Large holder, can influence proposals
        TokenHolder("whale_002", 300000),
        TokenHolder("small_holder_1", 100),
        TokenHolder("small_holder_2", 50),
    ]
    # Add some more small holders to simulate broader distribution
    for i in range(3, 10):
        token_holders.append(TokenHolder(f"small_holder_{i}", random.randint(10, 500)))

    print(f"Initialized {len(token_holders)} token holders.")

    # 2. Simulate proposal creation
    proposals = []
    next_proposal_id = 1

    # Simulate a legitimate proposal
    proposer_whale = random.choice([h for h in token_holders if h.balance >= TOTAL_TOKENS * MIN_VOTE_THRESHOLD])
    if proposer_whale:
        proposal_desc_legit = "Upgrade smart contract for efficiency improvements."
        proposals.append(Proposal(next_proposal_id, proposal_desc_legit, proposer_whale.address))
        print(f"\n[Proposal {next_proposal_id}] Created by {proposer_whale.address} (Balance: {proposer_whale.balance}): {proposal_desc_legit}")
        next_proposal_id += 1
    else:
        print("\nCould not find a token holder large enough to create a legitimate proposal.")

    # Simulate a malicious proposal (e.g., to drain funds, though this example won't simulate fund transfer)
    # This highlights the attack surface of *proposal creation* itself.
    proposer_malicious = random.choice(token_holders)
    proposal_desc_malicious = "Transfer 10% of treasury to attacker address."
    proposals.append(Proposal(next_proposal_id, proposal_desc_malicious, proposer_malicious.address))
    print(f"[Proposal {next_proposal_id}] Created by {proposer_malicious.address} (Balance: {proposer_malicious.balance}): {proposal_desc_malicious}")
    next_proposal_id += 1

    # 3. Simulate voting process for each proposal
    for proposal in proposals:
        print(f"\n--- Voting for Proposal {proposal.proposal_id} ---")
        total_voting_power = sum(h.balance for h in token_holders)
        current_quorum_power = 0

        # Simulate random voting behavior
        for holder in token_holders:
            # Decide if holder votes (e.g., 70% chance to vote)
            if random.random() < 0.7:
                # Decide vote direction (weighted by balance, but simplified here)
                vote_choice = random.choice(['yes', 'no'])
                if holder.address not in proposal.voters:
                    proposal.votes[vote_choice] += holder.balance
                    proposal.voters.add(holder.address)
                    current_quorum_power += holder.balance
                    # print(f"  {holder.address} voted {vote_choice} ({holder.balance} tokens)") # Uncomment for detailed voting

        print(f"Total voting power: {total_voting_power}")
        print(f"Quorum power reached: {current_quorum_power}")
        print(f"Vote counts: Yes - {proposal.votes['yes']}, No - {proposal.votes['no']}")

        # 4. Determine proposal outcome
        quorum_met = current_quorum_power >= (TOTAL_TOKENS * QUORUM_THRESHOLD)
        if quorum_met:
            total_votes_cast = proposal.votes['yes'] + proposal.votes['no']
            if total_votes_cast > 0:
                pass_percentage = proposal.votes['yes'] / total_votes_cast
                if pass_percentage >= SUCCESS_VOTE_PERCENT:
                    proposal.is_passed = True
                    print("Result: Proposal PASSED (Quorum met and sufficient 'yes' votes)")
                else:
                    proposal.is_passed = False
                    print("Result: Proposal FAILED (Quorum met but insufficient 'yes' votes)")
            else:
                proposal.is_passed = False
                print("Result: Proposal FAILED (Quorum met but no votes cast)")
        else:
            proposal.is_passed = False
            print("Result: Proposal FAILED (Quorum not met)")

    print("\n--- Simulation Complete ---")
    print("Key attack vectors observed:\n1. Malicious proposal creation by large token holders.\n2. Potential for vote manipulation or apathy leading to unexpected outcomes.\n3. The need for robust checks on proposal content and proposer identity.")

if __name__ == "__main__":
    simulate_governance_attack_surface()
