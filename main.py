import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(host='localhost', user='root', password='Tiger')
mycursor = mydb.cursor()

# Create database and table if they don't exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS ATM_MACHINE")
mycursor.execute("USE ATM_MACHINE")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS RECORDS (
        ACCONT_NO INT(4) PRIMARY KEY,
        PASSWORD INT(3),
        NAME VARCHAR(20),
        CR_AMT INT DEFAULT 0,
        WITHDRAWL INT DEFAULT 0,
        BALANCE INT DEFAULT 0
    )
""")

conn = mysql.connector.connect(host='localhost', user='root', password='Tiger', database='ATM_MACHINE')
c1 = conn.cursor()

print("=" * 90)
print(" WELCOME TO OUR ATM ")
print("=" * 90)
print("1. To create account")
print("2. To login")
print("3. Exit")
print("=" * 90)

# Main operation loop
while True:
    op = int(input("Enter your choice: "))
    print("=" * 90)

    if op == 1:
        c = "y"
        while c == "y":
            m = int(input("Enter a 4 digit number as account number: "))
            c1.execute(f"SELECT * FROM RECORDS WHERE ACCONT_NO={m}")
            data = c1.fetchall()
            if c1.rowcount == 1:
                print("=" * 90)
                print("This account number already exists:")
                c = input("Do you want to continue y/n: ")
                print("=" * 90)
                if c != "y":
                    print("Thank you. Please close this file before exiting.")
                    print("Visit again")
                    break
            else:
                name = input("Enter your name: ")
                passw = int(input("Enter your password: "))
                c1.execute(f"INSERT INTO RECORDS (ACCONT_NO, PASSWORD, NAME) VALUES ({m}, {passw}, '{name}')")
                conn.commit()
                print("=" * 90)
                print("Account successfully created")
                print("The minimum balance is 1000")
                s = int(input("Enter the money to be deposited: "))
                print("=" * 90)
                c1.execute(f"UPDATE RECORDS SET CR_AMT={s} WHERE ACCONT_NO={m}")
                c1.execute(f"UPDATE RECORDS SET BALANCE=CR_AMT-WITHDRAWL WHERE ACCONT_NO={m}")
                conn.commit()
                print("Successfully deposited")
                print("Thank you. Please close this file before exiting.")
                print("Visit again")
                break

    elif op == 2:
        y = "y"
        while y == "y":
            acct = int(input("Enter your account number: "))
            c1.execute(f"SELECT * FROM RECORDS WHERE ACCONT_NO={acct}")
            data = c1.fetchall()
            if c1.rowcount == 1:
                pas = int(input("Enter your password: "))
                c1.execute(f"SELECT PASSWORD FROM RECORDS WHERE ACCONT_NO={acct}")
                a = c1.fetchone()
                if pas == a[0]:
                    print("Successfully Logged In")
                    print("1. Depositing money")
                    print("2. Withdrawing money")
                    print("3. Transferring money")
                    print("4. Checking balance")
                    print("=" * 90)
                    r = int(input("Enter your choice: "))
                    print("=" * 90)

                    if r == 1:
                        amt = int(input("Enter the money to be deposited: "))
                        c1.execute(f"UPDATE RECORDS SET CR_AMT=CR_AMT + {amt} WHERE ACCONT_NO={acct}")
                        c1.execute(f"UPDATE RECORDS SET BALANCE=CR_AMT-WITHDRAWL WHERE ACCONT_NO={acct}")
                        conn.commit()
                        print("Successfully deposited")
                    elif r == 2:
                        amt = int(input("Enter the money to withdraw: "))
                        c1.execute(f"SELECT BALANCE FROM RECORDS WHERE ACCONT_NO={acct}")
                        m = c1.fetchone()
                        if amt > m[0]:
                            print(f"You have less than {amt}. Please try again.")
                        else:
                            c1.execute(f"UPDATE RECORDS SET BALANCE=BALANCE - {amt} WHERE ACCONT_NO={acct}")
                            c1.execute(f"UPDATE RECORDS SET WITHDRAWL={amt} WHERE ACCONT_NO={acct}")
                            conn.commit()
                            print("Please collect the amount.")
                    elif r == 3:
                        act = int(input("Enter the account number to be transferred: "))
                        c1.execute(f"SELECT * FROM RECORDS WHERE ACCONT_NO={act}")
                        if c1.rowcount == 1:
                            print(f"{act} number exists")
                            m = int(input("Enter the money to be transferred: "))
                            c1.execute(f"SELECT BALANCE FROM RECORDS WHERE ACCONT_NO={acct}")
                            c = c1.fetchone()
                            if m > c[0]:
                                print(f"You have less than {m}. Please try again.")
                            else:
                                c1.execute(f"UPDATE RECORDS SET BALANCE=BALANCE - {m} WHERE ACCONT_NO={acct}")
                                c1.execute(f"UPDATE RECORDS SET BALANCE=BALANCE + {m} WHERE ACCONT_NO={act}")
                                c1.execute(f"UPDATE RECORDS SET WITHDRAWL=WITHDRAWL + {m} WHERE ACCONT_NO={acct}")
                                c1.execute(f"UPDATE RECORDS SET CR_AMT=CR_AMT + {m} WHERE ACCONT_NO={act}")
                                conn.commit()
                                print("Successfully transferred")
                        else:
                            print("Account does not exist.")
                    elif r == 4:
                        c1.execute(f"SELECT BALANCE FROM RECORDS WHERE ACCONT_NO={acct}")
                        k = c1.fetchone()
                        print("Balance in your account =", k[0])
                    else:
                        print("Invalid choice.")
                else:
                    print("Wrong password")
            else:
                print("Your account does not exist.")
            y = input("Do you want to continue y/n: ")

    elif op == 3:
        print("Exiting")
        print("Please close this file before exiting.")
        c1.close()
        break

    else:
        print("Invalid choice. Please try again.")
