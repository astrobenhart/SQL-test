
# coding: utf-8

# # Test MySQL/Python Database

# ## Useful SQL commands
# 1. "CREATE DATABASE namedb" - creates a database called namedb
# 2. "CREATE TABLE inventory (sku INTEGER PRIMARY KEY, name TEXT, quantity INTEGER)" - creates a table called inventory and gives it columns called sku, which is given as the primary key and can only be an integer, name, the name of the product as text, and quantity, which can only be an integer.
# 3. "ALTER TABLE inventory ADD COLUMN link TEXT" - if we want to add a new column with the web links to each item to our inventory.
# 4. "INSERT INTO inventory (sku, name, quantity, link, catagory) VALUES (sk1, name1, quantity1, link1, catagory1)" - add an item (row) into these columns of inventory. This is actually done a little differently, you can see it below.
# 5. "SELECT * FROM inventory" - select everything in inventory, or replace * with column name to select just that column.
# 6. "SELECT * FROM inventory WHERE catagory ='catagory1'" - select all columns where the catagory is named 'catagory1'.
# 7. "SELECT * FROM inventory WHERE catagory LIKE '%cat%'" - select all columns where the catagory contains the wildcard 'cat'.
# 8. "DELETE FROM inventory WHERE name LIKE '%name%'" - delete all columns where the name contains the wildcard 'name'.
# 9. "UPDATE inventory SET quantity = '3' WHERE name = 'name'" - update the quantity of the item 'name' to 3.
# 10. "SELECT * FROM inventory LIMIT 2" - select all columns of first 2 rows in inventory
# 11. "SELECT * FROM inventory LIMIT 2 OFFSET 3" - select all columns of rows 4 and 5 in inventory
# 12. "DROP DATABASE namedb" - delete a database from MySQL
# 13. "SELECT users.name, products.name FROM users JOIN products ON users.fav = products.sku" - take the names of users amd products and stick them together using fav and sku of user and products, respectively.
# 14. "SELECT users.name, products.name FROM users LEFT JOIN products ON users.fav = products.sku" - Do the same as above but display all users
# 15. "SELECT users.name, products.name FROM users RIGHT JOIN products ON users.fav = products.sku" - Do the same as 13, but show all products.

# Import MySQL and login the the system MySQL server. Then create a database call storedb, this only has to be done once so is commented out below, if running for the first time, uncomment.

# In[7]:

import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  #needs to be the actual password you setup for MySQL, if its the below, then good luck to ya.
  passwd="password"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE storedb")


# You might find that the code stops running giving you this error "raise errors.ProgrammingError("Cursor is not connected")", this is common when playing around with the code. You probably just need to reconnect the cursor by running the code below

# In[26]:

mydb = mysql.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="storedb"
)
mycursor = mydb.cursor()


# print all db on system

# In[8]:

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)


# Now that storedb is made we can just log straight in by inserting database="storedb" into our connect step

# In[9]:

mydb = mysql.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="storedb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE inventory (sku INTEGER PRIMARY KEY, name TEXT, quantity INTEGER)")


# Add a new column for the web address

# In[10]:

mycursor.execute("ALTER TABLE inventory ADD COLUMN catagory TEXT")
mycursor.execute("ALTER TABLE inventory ADD COLUMN link TEXT")


# Now we want to add some data to our inventory

# In[11]:

# maintain %s even for ints, it is SQL not python
sql = "INSERT INTO inventory (sku, name, quantity, link, catagory) VALUES (%s, %s, %s, %s, %s)"
val = ("1", "100% cotton t-shirt black - L", "3", 'www.link1.ob.fake', "Tees - women")
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record inserted.")


# That was pretty slow, lets add multiple lines in at once

# In[12]:

val = [("2", "100% cotton t-shirt black - M", "12", "www.link2.ob.fake", "Tees - women"),
      ("3", "100% cotton t-shirt black - XL", "14", "www.link3.ob.fake", "Tees - women"),
      ("4", "100% cotton t-shirt black - XXL", "9", "www.link4.ob.fake", "Tees - women")]
mycursor.executemany(sql, val)
mydb.commit()

print(mycursor.rowcount, "was inserted.")


# Often after adding a few items it is useful to check the items id/SKU, so lets add a new item and do that.

# In[13]:

sql = "INSERT INTO inventory (sku, name, quantity, link, catagory) VALUES (%s, %s, %s, %s, %s)"
val = ("5", "black wallet", "10", 'www.link5.ob.fake', "Accessory - Wallets and Purrses")
mycursor.execute(sql, val)
mydb.commit()

print("last added SKU: ", mycursor.lastrowid


# lets now have a look at our whole table to get an overview

# In[16]:

mycursor.execute("SELECT * FROM inventory")

myresults = mycursor.fetchall()

for x in myresults:
    print(x)


# That's great and all but a bit messy, really we just want to see the SKU, name, and quantity

# In[17]:

mycursor.execute("SELECT sku, name, quantity FROM inventory")

myresults = mycursor.fetchall()

for x in myresults:
    print(x)


# Sometimes it is nice to just see one row, especially if you are unfamiliar with the data

# In[18]:

mycursor.execute("SELECT * FROM inventory")

myresult = mycursor.fetchone()

print(myresult)


# Now for some really interesting stuff, we want all the Wallets and Purrses in our inventory. We can use the catagory column we added earlier to help us here

# In[27]:

sql = "SELECT * FROM inventory WHERE catagory ='Accessory - Wallets and Purrses'"
mycursor.execute(sql)
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# If we just want to look at the shirts in our inventory we can just search for the wildcard 'Tees' in our catagory

# In[28]:

sql = "SELECT * FROM inventory WHERE catagory LIKE '%Tees%'"
mycursor.execute(sql)
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# When query values are provided by the user, you should escape the values.
# This is to prevent SQL injections, which is a common web hacking technique to destroy or misuse your database.
# The mysql.connector module has methods to escape query values. For example, use the placeholder %s

# In[29]:

sql = "SELECT * FROM inventory WHERE catagory =%s"
val = ('Accessory - Wallets and Purrses',)
mycursor.execute(sql, val)
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# Selecting things is great but we often want to sort them, this is a bit of a lame example as there is only two catagories but you get the idea, make it more complicated if you want.

# In[30]:

sql = "SELECT * FROM inventory ORDER BY catagory"
mycursor.execute(sql)
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# To sort in decending order just add DESC at the end of the SQL statement

# In[31]:

sql = "SELECT * FROM inventory ORDER BY catagory DESC"
mycursor.execute(sql)
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# For disconntinued products we may want to remove them from our inventory, I actually don't recommend this and would instead set the quantity to 0, but it is still important to know.

# In[32]:

sql = "DELETE FROM inventory WHERE name LIKE '%XXL%'"
mycursor.execute(sql)
mydb.commit()

print(mycursor.rowcount, "record(s) deleted")


# We should properly write it this way to prevent SQL injection too.

# In[34]:

sql = "DELETE FROM inventory WHERE name LIKE %s"
val = ('%XXL%',)
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record(s) deleted")


# We can also delete whole tables if we want, useful if creating temporary subsets and you don't want to keep them forever. I've commented them out because I don't actually want to delete the table.

# In[ ]:

#sql = "DROP TABLE inventory"
#mycursor.execute(sql)


# We can also delete tables only if they exist which can be nice if you don't want error returns

# In[ ]:

#sql = "DROP TABLE IF EXISTS inventory"
#mycursor.execute(sql)


# Probably one of the most used terms in SQL is UPDATE, for the simple reson that you will be updating lots of things, like when a sale is made or items restocked the quantity will change

# In[35]:

sql = "UPDATE inventory SET quantity = '3' WHERE name = 'black wallet'"
mycursor.execute(sql)
mydb.commit()

print(mycursor.rowcount, "record(s) affected")


# Now do it where no SQL injection can occur

# In[36]:

sql = "UPDATE inventory SET quantity = %s WHERE name = %s"
val = ('3', 'black wallet')
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record(s) affected")


# Now we only have 4 items, but lets say I wanted to print all but only see 2 of them.

# In[37]:

mycursor.execute("SELECT * FROM inventory LIMIT 2")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# Actually I wanted to skip the first one

# In[38]:

mycursor.execute("SELECT * FROM inventory LIMIT 2 OFFSET 1")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# So I want to show JOIN so lets create two example tables, users and products. The Users table will have an ID, name, and that persons favorite product. The Products table will have a SKU and name. The users ID auto increments for each new person, whereas the sku of the product is manually set. 

# In[46]:

#If you screw up just delete both tables here and start again
sql = "DROP TABLE users"
mycursor.execute(sql)
sql = "DROP TABLE products"
mycursor.execute(sql)


# In[47]:

mydb = mysql.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="storedb"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT, fav INTEGER)")
mycursor.execute("CREATE TABLE products (sku INTEGER PRIMARY KEY, name TEXT)")

sql = "INSERT INTO users (name, fav) VALUES (%s, %s)"
val = [("Chen", "154"),
      ("Dave", "153"),
      ("Ekta", "153"),
      ("Alex", "152"),
      ("Sean", "148")]
mycursor.executemany(sql, val)
mydb.commit()

print(mycursor.rowcount, "was inserted.")
print("")

mycursor.execute("SELECT * FROM users")
myresults = mycursor.fetchall()
for x in myresults:
    print(x)
print("")

sql = "INSERT INTO products (sku, name) VALUES (%s, %s)"
val = [("151", "apple"),
      ("152", "banana"),
      ("153", "orange"),
      ("154", "pear")]
mycursor.executemany(sql, val)
mydb.commit()

print(mycursor.rowcount, "was inserted.")
print("")

mycursor.execute("SELECT * FROM products")
myresults = mycursor.fetchall()
for x in myresults:
    print(x)
print("")

sql = " SELECT     users.name,     products.name     FROM users     JOIN products ON users.fav = products.sku"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print (x)


# In the output above you'll notice that we can't see Sean, this is because there was no match in products, if we wish to see all users then we have to use LEFT JOIN

# In[48]:

sql = " SELECT     users.name,     products.name     FROM users     LEFT JOIN products ON users.fav = products.sku"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print (x)


# If you want to return all products, and the users who have them as their favorite, even if no user has them as their favorite, use the RIGHT JOIN statement

# In[8]:

sql = " SELECT     users.name     products.name     FROM users     RIGHT JOIN products ON users.fav = products.sku"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print (x)


# ## Thats it for now, as you can see from the above it is very easy to integrate MySQL and Python. I would suggest now doing a full SQL course and trying to implement it all using the above methods or creating a usable stores inventory GUI frontend and Python/MySQL backend.
