import mysql.connector

# Connect to MySQL database with the correct collation
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    # collation='utf8mb4_unicode_ci'  # Use utf8mb4_unicode_ci for compatibility with MariaDB
)

mycursor = mydb.cursor()

# Create database and table if they don't exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS ATM_MACHINE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
mycursor.execute("USE ATM_MACHINE")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS RECORDS (
        ACCONT_NO INT(4) PRIMARY KEY,
        PASSWORD VARCHAR(6),
        NAME VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
        CR_AMT INT DEFAULT 0,
        WITHDRAWL INT DEFAULT 0,
        BALANCE INT DEFAULT 0
    )
""")

conn = mysql.connector.connect(host='localhost', user='root', password='root', database='ATM_MACHINE', collation='utf8mb4_unicode_ci')
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

    match op:
        case 1:
            c = "y"
            while c == "y":
                m = int(input("Enter a 4 digit number as account number: "))
                c1.execute("SELECT * FROM RECORDS WHERE ACCONT_NO = %s", (m,))
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
                    passw = input("Enter your password: ")
                    c1.execute("INSERT INTO RECORDS (ACCONT_NO, PASSWORD, NAME) VALUES (%s, %s, %s)", (m, passw, name))
                    conn.commit()
                    print("=" * 90)
                    print("Account successfully created")
                    print("The minimum balance is 1000")
                    s = int(input("Enter the money to be deposited: "))
                    print("=" * 90)
                    c1.execute("UPDATE RECORDS SET CR_AMT = %s WHERE ACCONT_NO = %s", (s, m))
                    c1.execute("UPDATE RECORDS SET BALANCE = CR_AMT - WITHDRAWL WHERE ACCONT_NO = %s", (m,))
                    conn.commit()
                    print("Successfully deposited")
                    print("Thank you. Please close this file before exiting.")
                    print("Visit again")
                    break

        case 2:
            y = "y"
            while y == "y":
                acct = int(input("Enter your account number: "))
                c1.execute("SELECT * FROM RECORDS WHERE ACCONT_NO = %s", (acct,))
                data = c1.fetchall()
                if c1.rowcount == 1:
                    pas = input("Enter your password: ")
                    c1.execute("SELECT PASSWORD FROM RECORDS WHERE ACCONT_NO = %s", (acct,))
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
                            c1.execute("UPDATE RECORDS SET CR_AMT = CR_AMT + %s WHERE ACCONT_NO = %s", (amt, acct))
                            c1.execute("UPDATE RECORDS SET BALANCE = CR_AMT - WITHDRAWL WHERE ACCONT_NO = %s", (acct,))
                            conn.commit()
                            print("Successfully deposited")
                        elif r == 2:
                            amt = int(input("Enter the money to withdraw: "))
                            c1.execute("SELECT BALANCE FROM RECORDS WHERE ACCONT_NO = %s", (acct,))
                            m = c1.fetchone()
                            if amt > m[0]:
                                print(f"You have less than {amt}. Please try again.")
                            else:
                                c1.execute("UPDATE RECORDS SET BALANCE = BALANCE - %s WHERE ACCONT_NO = %s", (amt, acct))
                                c1.execute("UPDATE RECORDS SET WITHDRAWL = %s WHERE ACCONT_NO = %s", (amt, acct))
                                conn.commit()
                                print("Please collect the amount.")
                        elif r == 3:
                            act = int(input("Enter the account number to be transferred: "))
                            c1.execute("SELECT * FROM RECORDS WHERE ACCONT_NO = %s", (act,))
                            if c1.rowcount == 1:
                                print(f"{act} number exists")
                                m = int(input("Enter the money to be transferred: "))
                                c1.execute("SELECT BALANCE FROM RECORDS WHERE ACCONT_NO = %s", (acct,))
                                c = c1.fetchone()
                                if m > c[0]:
                                    print(f"You have less than {m}. Please try again.")
                                else:
                                    c1.execute("UPDATE RECORDS SET BALANCE = BALANCE - %s WHERE ACCONT_NO = %s", (m, acct))
                                    c1.execute("UPDATE RECORDS SET BALANCE = BALANCE + %s WHERE ACCONT_NO = %s", (m, act))
                                    c1.execute("UPDATE RECORDS SET WITHDRAWL = WITHDRAWL + %s WHERE ACCONT_NO = %s", (m, acct))
                                    c1.execute("UPDATE RECORDS SET CR_AMT = CR_AMT + %s WHERE ACCONT_NO = %s", (m, act))
                                    conn.commit()
                                    print("Successfully transferred")
                            else:
                                print("Account does not exist.")
                        elif r == 4:
                            c1.execute("SELECT BALANCE FROM RECORDS WHERE ACCONT_NO = %s", (acct,))
                            k = c1.fetchone()
                            print("Balance in your account =", k[0])
                        else:
                            print("Invalid choice.")
                    else:
                        print("Wrong password")
                else:
                    print("Your account does not exist.")
                y = input("Do you want to continue y/n: ")

        case 3:
            print("Exiting")
            print("Please close this file before exiting.")
            c1.close()
            break

        case _:
            print("Invalid choice. Please try again.")
    op = int(input("Enter your choice: "))
