import tkinter as tk
from local_tracker import Receiver, Tracker

def move():
    can.delete("temp")
    
    try:
        xpos = float(xpos_ent.get())
        ypos = float(ypos_ent.get())
    except ValueError:
        print("Invalid input! Enter numeric values.")
        return

    patient1.move_to(xpos, ypos)

    try:
        loc = patient1.find_position(receivers)
    except ValueError as e:
        print(f"Error: {e}")
        return

    p_lbl.place(x = loc[0], y = loc[1])
    p_lbl.config(text=patient1.id)
    # Draw tracker position as a circle
    tracker_radius = 10
    can.create_oval(loc[0] - tracker_radius, loc[1] - tracker_radius, 
                    loc[0] + tracker_radius, loc[1] + tracker_radius, 
                    outline="blue", fill="blue", tags="temp")

    for rec_id, rec in receivers.items():
        receiver_labels[rec_id].config(text=f"{rec_id}: {round(patient1.report(rec), 2)}")

    x_lbl.config(text=f"x = {round(loc[0], 2)}")
    y_lbl.config(text=f"y = {round(loc[1], 2)}")

    for rec_id, rec in receivers.items():
        can.create_line(loc[0], loc[1], rec.x, rec.y, width=1, fill="blue", tags="temp")

# Initialize receivers
receivers = {}
receivers["Rec1"] = Receiver("Rec1", 200, 200)
receivers["Rec2"] = Receiver("Rec2", 200, 400)
receivers["Rec3"] = Receiver("Rec3", 400, 200)
receivers["Rec4"] = Receiver("Rec4", 400, 400)
receivers["Rec5"] = Receiver("Rec5", 600, 200)
receivers["Rec6"] = Receiver("Rec6", 600, 400)

# Tkinter window
root = tk.Tk()
root.title("Local Tracker Tester")
root.geometry("800x700")

# Frame with labels and button
bot_frame = tk.Frame(root)
bot_frame.pack(side="bottom", fill=tk.BOTH)

xpos_lbl = tk.Label(bot_frame, text="xPos = ")
xpos_ent = tk.Entry(bot_frame, width=10)
xpos_ent.insert(0, 550)
ypos_lbl = tk.Label(bot_frame, text="yPos = ")
ypos_ent = tk.Entry(bot_frame, width=10)
ypos_ent.insert(0, 50)
move_btn = tk.Button(bot_frame, text="MOVE", command=move)
x_lbl = tk.Label(bot_frame, text="x = ?")
y_lbl = tk.Label(bot_frame, text="y = ?")

xpos_lbl.grid(row=1, column=1)
xpos_ent.grid(row=1, column=2)
ypos_lbl.grid(row=1, column=3)
ypos_ent.grid(row=1, column=4)
move_btn.grid(row=1, column=5)
x_lbl.grid(row=0, column=2)
y_lbl.grid(row=0, column=4)

# Background image
bg_image = tk.PhotoImage(file="./images/sample_layout.png")

# main display
can = tk.Canvas(root, width=800, height=600)
can.pack(side="top", fill=tk.BOTH)
can.create_image(0, 0, image=bg_image, anchor="nw")

# Dictionary to store the labels of the reveivers
receiver_labels = {}  
for rec_id, receiver in receivers.items():
    receiver_labels[rec_id] = tk.Label(can, text=rec_id, bg="green")
    receiver_labels[rec_id].place(x=receiver.x, y=receiver.y)

# tracker representation
p_lbl = tk.Label(can)

patient1 = Tracker("John", 0, 0)

root.mainloop()