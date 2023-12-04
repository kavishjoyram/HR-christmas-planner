import tkinter as tk
from tkinter import messagebox
import csv
import os

class HRApp:
    def __init__(self, master):
        self.master = master
        self.master.title("HR Event Participation App")

        # Initialize participant list
        self.participant_list = []

        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.label_name = tk.Label(self.master, text="Name:")
        self.label_participation = tk.Label(self.master, text="Participation:")

        # Entry Widgets
        self.entry_name = tk.Entry(self.master)
        self.var_participation = tk.StringVar(value="Yes")
        self.entry_participation = tk.Entry(self.master, textvariable=self.var_participation)

        # Buttons
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        self.show_participants_button = tk.Button(self.master, text="Show Participants", command=self.show_participants)
        self.save_button = tk.Button(self.master, text="Save Data", command=self.save_data)
        self.load_button = tk.Button(self.master, text="Load Data", command=self.load_data)
        self.export_csv_button = tk.Button(self.master, text="Export to CSV", command=self.export_to_csv)

        # Layout
        self.label_name.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.label_participation.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.entry_participation.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        self.submit_button.grid(row=2, column=1, pady=10)
        self.show_participants_button.grid(row=3, column=1, pady=10)
        self.save_button.grid(row=4, column=1, pady=10)
        self.load_button.grid(row=5, column=1, pady=10)
        self.export_csv_button.grid(row=6, column=1, pady=10)

    def submit(self):
        name = self.entry_name.get()
        participation = self.var_participation.get()

        if name and participation:
            self.participant_list.append({"name": name, "participation": participation})
            messagebox.showinfo("Submission Successful", f"Thank you, {name}! Your participation status is recorded as {participation}.")
            self.clear_entries()
        else:
            messagebox.showwarning("Incomplete Form", "Please fill in both name and participation status.")

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.var_participation.set("Yes")

    def show_participants(self):
        if not self.participant_list:
            messagebox.showinfo("No Participants", "No participants recorded yet.")
            return

        filter_status = messagebox.askyesno("Filter Participants", "Do you want to filter participants by participation status?")
        filtered_list = self.participant_list if not filter_status else self.filter_participants()

        if filtered_list:
            participant_info = "\n".join([f"{participant['name']} - {participant['participation']}" for participant in filtered_list])
            messagebox.showinfo("Participant List", f"Participant List:\n{participant_info}")

    def filter_participants(self):
        filter_status = messagebox.askquestion("Filter Participants", "Filter by 'Yes' or 'No'?")
        return [participant for participant in self.participant_list if participant["participation"].lower() == filter_status.lower()]

    def save_data(self):
        try:
            with open("participant_data.txt", "w") as file:
                for participant in self.participant_list:
                    file.write(f"{participant['name']},{participant['participation']}\n")
            messagebox.showinfo("Data Saved", "Participant data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")

    def load_data(self):
        try:
            file_path = "participant_data.txt"
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    self.participant_list = []
                    for line in file:
                        name, participation = line.strip().split(',')
                        self.participant_list.append({"name": name, "participation": participation})
                messagebox.showinfo("Data Loaded", "Participant data loaded successfully.")
            else:
                messagebox.showinfo("No Data", "No participant data found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading data: {e}")

    def export_to_csv(self):
        try:
            if self.participant_list:
                with open("participant_data.csv", "w", newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(["Name", "Participation"])
                    for participant in self.participant_list:
                        csv_writer.writerow([participant['name'], participant['participation']])
                messagebox.showinfo("Export Successful", "Data exported to CSV successfully.")
            else:
                messagebox.showinfo("No Data", "No participant data to export.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exporting data to CSV: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HRApp(root)
    root.mainloop()
