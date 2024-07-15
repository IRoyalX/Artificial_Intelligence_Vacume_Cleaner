from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

row = col = rooms = None

@app.route('/', methods=['GET', 'POST'])
def construct():
    global row, col
    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])
        return redirect(url_for('prepare'))
    return render_template('construct.html')
    

@app.route('/prepare', methods=['GET', 'POST'])
def prepare():
    global row, col, rooms
    if request.method == 'POST':
       for i in request.form:
           i = eval("[" + i + "]")
           rooms[i[0]-1][i[1]-1] += ' id=dirty'
       return render_template('prepare.html', rooms= rooms, title= "Select V.C. Position...", sub= "hidden", id="clean", type="submit")
    rooms = []
    for i in range(row):
        r = []
        for j in range(col):
            r.append(f'{i+1},{j+1}')
        rooms.append(r)
    return render_template('prepare.html', rooms = rooms, title= "Select dirty room(s)...", sub = None, id="prepare", type="checkbox")


@app.route('/clean', methods=['GET', 'POST'])
def clean():
    global row, col, rooms
    x = i = eval('[' + next(iter(request.form.to_dict())) + ']')[0]-1
    y = j = eval('[' + next(iter(request.form.to_dict())) + ']')[1]-1
    
    inf = [[i, j]]
    mvs = []
    def locate():
        if j > inf[-1][1]:
            mvs.append("RIGHT")
            inf.append([i, j])
        elif j < inf[-1][1]:
            mvs.append("LEFT")
            inf.append([i, j])
        elif i > inf[-1][0]:
            mvs.append("DOWN")
            inf.append([i, j])
        elif i < inf[-1][0]:
            mvs.append("UP")
            inf.append([i, j])        

    def move(inx):
        nonlocal i, j
        rm = 1
        if i%2 == 0:
            rm = 0
        for i in inx[0]:
            if i%2 == rm:
                for j in inx[1]:
                    locate()
                          
            else:
                for j in inx[2]:
                    locate()
            locate()

    move([range(i, row), range(j, col), range(col-1, j-1, -1)])

    if j != y:
        for j in range(col-2, y-1, -1):
                    locate()

    if j != 0:
        move([range(row-1, x-1, -1), range(y-1, -1, -1), range(0, y)])

    if i != x:
        for i in range(row-2, x-1, -1):
                    locate()
    elif j != 0:
        for j in range(y-2, -1, -1):
                    locate()

    move([range(i-1, -1, -1), range(col-1, -1, -1), range(col)])

    return render_template('clean.html', rooms=rooms, inf=inf, mvs=mvs, col=col)

if __name__ == '__main__':
    app.run(debug=True)
