def calculate_electricity_split():
    print("--- Electricity Bill Splitter ---\n")

    # --- INPUTS ---
    # You can hardcode these if your rates never change
    try:
        unit_rate = float(input("Enter electricity unit rate (e.g., 0.28 for 28p/kWh): "))
        standing_charge_daily = float(input("Enter daily standing charge (e.g., 0.45 for 45p/day): "))
        bill_days = int(input("Enter number of days in this billing period: "))
        
        total_kwh_usage = float(input("Enter TOTAL kWh usage for the flat: "))
        pc_kwh_usage = float(input("Enter YOUR PC's kWh usage (from Tapo app): "))
    except ValueError:
        print("\nError: Please enter valid numbers.")
        return

    # --- CALCULATIONS ---
    
    # 1. Calculate the fixed costs (Standing Charge)
    total_standing_charge_cost = standing_charge_daily * bill_days

    # 2. Calculate the energy costs
    # Note: We calculate total energy cost based on usage * rate
    total_energy_cost = total_kwh_usage * unit_rate
    
    # 3. Calculate specific cost of the PC
    pc_cost = pc_kwh_usage * unit_rate

    # 4. Calculate the Total Bill Calculation
    # (Standing Charge + All Energy)
    calculated_total_bill = total_standing_charge_cost + total_energy_cost

    # 5. Determine the "Shared" portion
    # The shared portion is the Total Bill minus the specific PC cost you are responsible for
    shared_cost = calculated_total_bill - pc_cost

    # 6. The Split
    # Girlfriend pays half of the shared cost
    girlfriend_pay = shared_cost / 2
    
    # You pay half the shared cost PLUS the full PC cost
    your_pay = (shared_cost / 2) + pc_cost

    # --- OUTPUT ---
    print("\n" + "="*30)
    print(f"💰 BILL BREAKDOWN")
    print("="*30)
    print(f"Total Bill (Calculated):  £{calculated_total_bill:.2f}")
    print(f"  - Standing Charge:      £{total_standing_charge_cost:.2f}")
    print(f"  - Total Energy Cost:    £{total_energy_cost:.2f}")
    print("-" * 30)
    print(f"🖥️  YOUR PC COST:         £{pc_cost:.2f}")
    print(f"🏠 SHARED COST:          £{shared_cost:.2f}")
    print("="*30)
    print(f"👉 YOU PAY:               £{your_pay:.2f}")
    print(f"👉 GIRLFRIEND PAYS:       £{girlfriend_pay:.2f}")
    print("="*30)

if __name__ == "__main__":
    calculate_electricity_split()
