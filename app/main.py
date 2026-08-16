from app.agent import BangaliGamerAgent
from app.knowledge import save_knowledge

def main():
    print("==================================================")
    print("   BANGALI GAMER AI - PHASE 3 (DYNAMIC KNOWLEDGE) ")
    print("==================================================")
    print("Select Login Mode:")
    print("1. Customer Mode (Normal Chat)")
    print("2. Admin Mode (Teach AI & Update Knowledge)")
    
    mode = input("\nEnter Mode (1 or 2): ").strip()
    is_admin = True if mode == '2' else False
    
    agent = BangaliGamerAgent(is_admin=is_admin)
    user_name = "Admin" if is_admin else "Customer"
    
    print(f"\n[{user_name} Mode Activated] Agent started! (Type 'exit' to quit)\n")
    
    while True:
        try:
            user_input = input(f"{user_name}: ")
            
            if user_input.lower() in ['exit', 'quit']:
                print("System: Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            print("Agent: Thinking...")
            response = agent.get_response(user_input)
            
            # --- THE MAGIC KNOWLEDGE SAVER ---
            if is_admin and "[SAVE_KNOWLEDGE:" in response:
                start_idx = response.find("[SAVE_KNOWLEDGE:") + 16
                end_idx = response.find("]", start_idx)
                
                if end_idx != -1:
                    new_fact = response[start_idx:end_idx].strip()
                    save_knowledge(new_fact) # Saving to txt file
                    
                    # Hide the raw tag from the terminal and show a cool notification
                    response = response[:response.find("[SAVE_KNOWLEDGE:")].strip()
                    response += f"\n\n✅ [System Notification: '{new_fact}' successfully saved to Knowledge Base!]"
            
            print(f"\nBangali Gamer AI:\n{response}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nShutting down system...")
            break

if __name__ == "__main__":
    main()