from flask import Flask, redirect, render_template, request
import sqlite3

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

@app.route("/")
def homepage():
    return render_template("grocery_index.html")

@app.route("/grocery-list/view-list")
def tdl():
    con = sqlite3.connect("groceries.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT items.item_id, items.completed, items.item_name, items.quantity, stores.store_name, stores.store_adress FROM stores JOIN items ON stores.store_id = items.store_id")
    rows = cur.fetchall()
    con.commit()
    con.close
    return render_template("grocery_list.html", rows=rows)

@app.route("/completed_item", methods=["GET", "POST"])
def completed():
    if request.method == 'POST':
        con = sqlite3.connect("groceries.db")
        completed = request.form['completed_value']
        item_id = request.form['item_id']
        con.execute("UPDATE items SET completed = ? WHERE item_id = ?", (completed, item_id))
        con.commit()
        con.close()
    return redirect("/grocery-list/view-list")