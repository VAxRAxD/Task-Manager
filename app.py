import typer
from typer.models import Default

app=typer.Typer()

@app.callback(invoke_without_command=True)
@app.command()
def help(ctx: typer.Context):
    add="./task add 2 hello world    # Add a new item with priority 2 and text \"hello world\" to the list"
    ls="./task ls                   # Show incomplete priority list items sorted by priority in ascending order"
    delete="./task del INDEX            # Delete the incomplete item with the given index"
    done="./task done INDEX           # Mark the incomplete item with the given index as complete"
    help="./task help                 # Show usage"
    report="./task report               # Statistics"
    if ctx.invoked_subcommand is None:
        print(f"{add}\n{ls}\n{delete}\n{done}\n{help}\n{report}")

@app.command("add")
def add( priority: str,name: str):
    tasks=[]
    with open("todo.txt","r") as todo:
        file=todo.readlines()
        if len(file)>0:
            todo.seek(0)
            for line in file:
                number,name_,priority_=map(str,line.split("|"))
                priority_=int(priority_.replace("\n",""))
                tasks.append([name_,priority_])
    tasks.append([name,int(priority)])
    tasks=(sorted(tasks,key=lambda x:x[1]))
    with open('todo.txt','w') as task:
        for i in range(len(tasks)):
            task.write(str(i+1)+"|"+str(tasks[i][0])+"|"+str(tasks[i][1])+"\n")
    print(f"Added task: \"{name}\" with priority {priority}")

@app.command("del")
def delete(number: int):
    with open("todo.txt","r") as task:
        file = task.readlines()
        task.seek(0)
        tasks=[]
        for line in file:
            number_,name_,priority_=map(str,line.split("|"))
            priority_=int(priority_.replace("\n",""))
            tasks.append([name_,priority_])
        jump=1
        with open("todo.txt",'w') as file:
            for i in range(len(tasks)):
                if i+1==number:
                    delete=tasks[i][0]
                    jump=0
                    continue
                else:
                    file.write(str(i+jump)+"|"+str(tasks[i][0])+"|"+str(tasks[i][1])+"\n")
    print(f"Deleted task #{number}")

@app.command("done")
def done(number: int):
    with open("todo.txt","r") as task:
        file = task.readlines()
        task.seek(0)
        tasks=[]
        for line in file:
            number_,name_,priority_=map(str,line.split("|"))
            priority_=int(priority_.replace("\n",""))
            tasks.append([name_,priority_])
        jump=1
        with open("todo.txt",'w') as file:
            for i in range(len(tasks)):
                if i+1==number:
                    jump=0
                    finished=tasks[i][0]
                    continue
                else:
                    file.write(str(i+jump)+"|"+str(tasks[i][0])+"|"+str(tasks[i][1])+"\n")
        tasks=[finished]
        with open("complete.txt",'r') as task:
            file = task.readlines()
            task.seek(0)
            if len(file)>0:
                for line in file:
                    number_,name=map(str,line.split("|"))
                    tasks.append(name)
        with open("complete.txt",'w') as file:
            for i in range(len(tasks)):
                file.write(str(i+1)+"|"+str(tasks[i])+"\n")
    print(f"Marked item as done.")

@app.command("report")
def report():
    pending=0
    pending_list=""
    complete=0
    complete_list=""
    with open("todo.txt","r") as todo:
        file=todo.readlines()
        todo.seek(0)
        for line in file:
            pending+=1
            number_,name_,priority_=map(str,line.split("|"))
            priority_=int(priority_.replace("\n",""))
            pending_list+=f"{number_}. {name_} [{priority_}]\n"
    with open("complete.txt","r") as todo:
        file=todo.readlines()
        todo.seek(0)
        for line in file:
            complete+=1
            number_,name_=map(str,line.split("|"))
            complete_list+=f"{number_}. {name_}"
    print(f"Pending : {pending}\n{pending_list}\nComplete: {complete}\n{complete_list}")

@app.command("ls")
def ls():
    pending_list=""
    with open("todo.txt","r") as todo:
        file=todo.readlines()
        todo.seek(0)
        for line in file:
            number_,name_,priority_=map(str,line.split("|"))
            priority_=int(priority_.replace("\n",""))
            pending_list+=f"{number_}. {name_} [{priority_}]\n"
    print(pending_list)

if __name__=="__main__":
    app()