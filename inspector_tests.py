from time import time

timer = time()
print("Importing required modules...")
from inspector import Inspector, DEFAULTS
print(f"Done ({(time() - timer):.5}s).\n")

# Variable settings:

try:
	start = int(input("[Starting size] Input an integer value greater than 2: "))
	assert start > 2
except Exception:
	print("Switching to default value...")
	start = DEFAULTS["start"]

try:
	cycles = int(input("[Total cycles] Input a positive integer value: "))
	assert cycles > 0
except Exception:
	print("Switching to default value...")
	cycles = DEFAULTS["cycles"]

try:
	ratio = int(input("[Ideal ratio] Input a float value greater than 2: "))
	assert ratio > 0
except Exception:
	print("Switching to default value...")
	ratio = DEFAULTS["ratio"]

try:
	constant = bool(int(input("Should the size of the array remain constant? (1/0) ")))
except Exception:
	print("Switching to default value...")
	ratio = DEFAULTS["constant"]

try:
	show_image = bool(int(input("Should images be shown? (1/0) ")))
except Exception:
	print("Switching to default value...")
	ratio = DEFAULTS["show_image"]

try:
	save_image = bool(int(input("Should images be saved? (1/0) ")))
except Exception:
	print("Switching to default value...")
	ratio = DEFAULTS["save_image"]

try:
	logger = bool(int(input("Should the process be logged? (1/0) ")))
except Exception:
	print("Switching to default value...")
	ratio = DEFAULTS["logger"]


# Main object and helper functions' definition:

timer = time()
print("\nGenerating objects...")
obj = Inspector(cycles=cycles, start=start, constant=constant, ratio=ratio,
	logger=logger)
print(f"Done ({(time() - timer):.5}s).\n")

timer = time()
print("Performing initial benchmark...")
obj.benchmark()
print(f"Done ({(time() - timer):.5}s).\n")

high = lambda: obj.display(max(obj.mazes, key=lambda x: x["ratio"]))
low = lambda: obj.display(min(obj.mazes, key=lambda x: x["ratio"]))

def dfs_handler(obj=obj):
	try:
		index = int(input("Input an index: "))
		obj.mazes[index]["maze"].dfs()
	except Exception:
		print("[ERROR]: Invalid index. Returning to menu...")

def gbfs_handler(obj=obj):
	try:
		index = int(input("Input an index: "))
		obj.mazes[index]["maze"].gbfs()
	except Exception:
		print("[ERROR]: Invalid index. Returning to menu...")

def image_handler(obj=obj, show_image=show_image, save_image=save_image):
	try:
		index = int(input("Input an index: "))
		assert 0 <= index <= len(obj.mazes)
	except Exception:
		print("[ERROR]: Invalid index. Returning to menu...")

	obj.mazes[index]["maze"].image(
		show_image=show_image, save_image=save_image
	)


# Menu:

options = (
	("Benchmark utility", obj.benchmark),
	("Comparison plot display", obj.display_plot),
	("Generated mazes' list", obj.list),
	("Get the lowest ratio maze", low),
	("Get the highest ratio maze", high),
	("Perform DF search", dfs_handler),
	("Perform GBF search", gbfs_handler),
	("Display maze on image", image_handler),
	("Exit: ", quit)
)


# Interface's mainloop:

while True:
	print("\nMenu:")
	for index, option in enumerate(options):
		print(f"{index + 1} :: {option[0]}")

	try:
		index = int(input("\nSelect an index: ")) - 1
		options[index][1]()
	except IndexError:
		print("[ERROR]: Invalid index, try again...")
	except Exception:
		print("[ERROR]: Undefined error exception. Fatal crash.")
		quit()

