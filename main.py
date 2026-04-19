"""
Student Profile Management System
Fundamentals of Data Science - Final Assessment Project
Module Code: UFCFK1-15-0

Features:
- Login system with admin/student roles
- CRUD operations for student records
- Grade management and ECA tracking
- Performance Analytics Dashboard with matplotlib
- OOP design with inheritance
- File handling and exception handling
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ============================================================
# FILE PATHS
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "sample_data")

USERS_FILE = os.path.join(DATA_DIR, "users.txt")
GRADES_FILE = os.path.join(DATA_DIR, "grades.txt")
ECA_FILE = os.path.join(DATA_DIR, "eca.txt")
PASSWORDS_FILE = os.path.join(DATA_DIR, "passwords.txt")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(CHARTS_DIR, exist_ok=True)

# ============================================================
# UTILITY: FILE HANDLER
# ============================================================
class FileHandler:
    """Handles all file read/write operations with exception handling."""

    @staticmethod
    def read_file(filepath):
        """Read all lines from a file, return list of lines."""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            return [line.strip() for line in lines if line.strip()]
        except FileNotFoundError:
            print(f"[Error] File not found: {filepath}")
            return []
        except PermissionError:
            print(f"[Error] Permission denied: {filepath}")
            return []
        except Exception as e:
            print(f"[Error] Could not read {filepath}: {e}")
            return []

    @staticmethod
    def write_file(filepath, lines):
        """Write list of lines to a file."""
        try:
            with open(filepath, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            return True
        except Exception as e:
            print(f"[Error] Could not write to {filepath}: {e}")
            return False

    @staticmethod
    def append_file(filepath, line):
        """Append a single line to a file."""
        try:
            with open(filepath, 'a') as f:
                f.write(line + '\n')
            return True
        except Exception as e:
            print(f"[Error] Could not append to {filepath}: {e}")
            return False


# ============================================================
# BASE CLASS: Person
# ============================================================
class Person:
    """Base class representing a person in the system."""

    def __init__(self, user_id, name, age, address, phone):
        self._user_id = user_id
        self._name = name
        self._age = age
        self._address = address
        self._phone = phone

    # --- Properties ---
    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    def display_info(self):
        """Display personal information."""
        print(f"  ID      : {self._user_id}")
        print(f"  Name    : {self._name}")
        print(f"  Age     : {self._age}")
        print(f"  Address : {self._address}")
        print(f"  Phone   : {self._phone}")

    def to_file_string(self, role):
        """Return string for users.txt"""
        return f"{self._user_id},{self._name},{self._age},{self._address},{self._phone},{role}"


# ============================================================
# DERIVED CLASS: Student (inherits Person)
# ============================================================
class Student(Person):
    """Represents a student, inheriting from Person."""

    def __init__(self, user_id, name, age, address, phone):
        super().__init__(user_id, name, age, address, phone)
        self._grades = {}   # subject -> mark
        self._eca = []      # list of activities

    @property
    def grades(self):
        return self._grades

    @grades.setter
    def grades(self, grades_dict):
        self._grades = grades_dict

    @property
    def eca(self):
        return self._eca

    @eca.setter
    def eca(self, eca_list):
        self._eca = eca_list

    def average_grade(self):
        """Calculate average grade across all subjects."""
        if not self._grades:
            return 0
        return sum(self._grades.values()) / len(self._grades)

    def display_grades(self):
        """Display student's grades."""
        if not self._grades:
            print("  No grades recorded.")
            return
        print("  Subject           | Marks")
        print("  " + "-" * 35)
        for subject, mark in self._grades.items():
            print(f"  {subject:<20}| {mark}")
        print(f"  {'Average':<20}| {self.average_grade():.2f}")

    def display_eca(self):
        """Display student's extracurricular activities."""
        if not self._eca:
            print("  No ECA activities recorded.")
            return
        print("  Extracurricular Activities:")
        for i, activity in enumerate(self._eca, 1):
            print(f"    {i}. {activity}")


# ============================================================
# DERIVED CLASS: Admin (inherits Person)
# ============================================================
class Admin(Person):
    """Represents an admin user, inheriting from Person."""

    def __init__(self, user_id, name, age, address, phone):
        super().__init__(user_id, name, age, address, phone)


# ============================================================
# DATA MANAGER
# ============================================================
class DataManager:
    """Manages loading and saving data from/to text files."""

    SUBJECTS = ["Mathematics", "Physics", "Programming", "English", "Data Science"]

    def __init__(self):
        self.students = {}  # user_id -> Student
        self.admins = {}    # user_id -> Admin
        self.passwords = {} # username -> password
        self.file_handler = FileHandler()

    def load_all(self):
        """Load all data from files."""
        self._load_passwords()
        self._load_users()
        self._load_grades()
        self._load_eca()

    # --- Loading methods ---
    def _load_passwords(self):
        lines = self.file_handler.read_file(PASSWORDS_FILE)
        for line in lines:
            parts = line.split(',')
            if len(parts) == 2:
                self.passwords[parts[0].strip()] = parts[1].strip()

    def _load_users(self):
        lines = self.file_handler.read_file(USERS_FILE)
        for line in lines:
            parts = line.split(',')
            if len(parts) == 6:
                uid, name, age, address, phone, role = [p.strip() for p in parts]
                try:
                    age = int(age)
                except ValueError:
                    age = 0
                if role.lower() == 'student':
                    self.students[uid] = Student(uid, name, age, address, phone)
                elif role.lower() == 'admin':
                    self.admins[uid] = Admin(uid, name, age, address, phone)

    def _load_grades(self):
        lines = self.file_handler.read_file(GRADES_FILE)
        for line in lines:
            parts = line.split(',')
            if len(parts) == 7:
                uid = parts[0].strip()
                if uid in self.students:
                    grades = {}
                    for i, subject in enumerate(self.SUBJECTS):
                        try:
                            grades[subject] = float(parts[i + 1].strip())
                        except (ValueError, IndexError):
                            grades[subject] = 0
                    # Semester stored in index 6
                    self.students[uid].grades = grades

    def _load_eca(self):
        lines = self.file_handler.read_file(ECA_FILE)
        for line in lines:
            parts = line.split(',', 1)
            if len(parts) == 2:
                uid = parts[0].strip()
                activities = [a.strip() for a in parts[1].split(';') if a.strip()]
                if uid in self.students:
                    self.students[uid].eca = activities

    # --- Saving methods ---
    def save_users(self):
        lines = []
        for uid, admin in self.admins.items():
            lines.append(admin.to_file_string("admin"))
        for uid, student in self.students.items():
            lines.append(student.to_file_string("student"))
        self.file_handler.write_file(USERS_FILE, lines)

    def save_grades(self):
        lines = []
        for uid, student in self.students.items():
            marks = [str(student.grades.get(sub, 0)) for sub in self.SUBJECTS]
            semester = "1"
            lines.append(f"{uid},{','.join(marks)},{semester}")
        self.file_handler.write_file(GRADES_FILE, lines)

    def save_eca(self):
        lines = []
        for uid, student in self.students.items():
            if student.eca:
                lines.append(f"{uid},{';'.join(student.eca)}")
        self.file_handler.write_file(ECA_FILE, lines)

    def save_passwords(self):
        lines = [f"{u},{p}" for u, p in self.passwords.items()]
        self.file_handler.write_file(PASSWORDS_FILE, lines)

    def save_all(self):
        self.save_users()
        self.save_grades()
        self.save_eca()
        self.save_passwords()

    # --- ID generation ---
    def generate_student_id(self):
        existing = [int(uid[1:]) for uid in self.students if uid.startswith('S') and uid[1:].isdigit()]
        next_num = max(existing, default=0) + 1
        return f"S{next_num:03d}"

    # --- Authenticate ---
    def authenticate(self, username, password):
        """Returns ('admin', Admin) or ('student', Student) or (None, None)."""
        if username in self.passwords and self.passwords[username] == password:
            if username in self.admins:
                return 'admin', self.admins[username]
            elif username in self.students:
                return 'student', self.students[username]
        return None, None


# ============================================================
# ANALYTICS ENGINE (Task 2 - Performance Analytics Dashboard)
# ============================================================
class AnalyticsEngine:
    """Generates charts and analytics for admin users."""

    def __init__(self, data_manager):
        self.dm = data_manager

    def show_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("  PERFORMANCE ANALYTICS DASHBOARD")
            print("=" * 50)
            print("  1. Subject-wise Average Grades (Bar Chart)")
            print("  2. Individual Student Grade Comparison")
            print("  3. Grade Distribution (Box Plot)")
            print("  4. ECA Impact on Academic Performance")
            print("  5. Performance Alerts (Below Threshold)")
            print("  6. Top Performers Ranking")
            print("  7. Back to Admin Menu")
            print("-" * 50)

            choice = input("  Enter choice: ").strip()
            if choice == '1':
                self.subject_average_chart()
            elif choice == '2':
                self.student_grade_comparison()
            elif choice == '3':
                self.grade_distribution()
            elif choice == '4':
                self.eca_impact_analysis()
            elif choice == '5':
                self.performance_alerts()
            elif choice == '6':
                self.top_performers()
            elif choice == '7':
                break
            else:
                print("  Invalid choice.")

    def subject_average_chart(self):
        """Bar chart of average grades per subject."""
        subjects = DataManager.SUBJECTS
        averages = []
        for sub in subjects:
            marks = [s.grades.get(sub, 0) for s in self.dm.students.values() if s.grades]
            avg = sum(marks) / len(marks) if marks else 0
            averages.append(avg)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12']
        bars = ax.bar(subjects, averages, color=colors, edgecolor='white', linewidth=1.5)

        for bar, val in zip(bars, averages):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f'{val:.1f}', ha='center', va='bottom', fontweight='bold')

        ax.set_title('Average Grades Per Subject', fontsize=16, fontweight='bold', pad=15)
        ax.set_ylabel('Average Marks', fontsize=12)
        ax.set_ylim(0, 110)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, 'subject_averages.png')
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  Chart saved: {path}")

    def student_grade_comparison(self):
        """Grouped bar chart comparing all students."""
        students = list(self.dm.students.values())
        if not students:
            print("  No students found.")
            return

        subjects = DataManager.SUBJECTS
        x = np.arange(len(subjects))
        width = 0.8 / len(students)

        fig, ax = plt.subplots(figsize=(12, 6))
        colors = plt.cm.Set2(np.linspace(0, 1, len(students)))

        for i, student in enumerate(students):
            marks = [student.grades.get(sub, 0) for sub in subjects]
            offset = (i - len(students) / 2 + 0.5) * width
            ax.bar(x + offset, marks, width, label=student.name, color=colors[i])

        ax.set_xticks(x)
        ax.set_xticklabels(subjects, rotation=15)
        ax.set_title('Student Grade Comparison', fontsize=16, fontweight='bold')
        ax.set_ylabel('Marks')
        ax.set_ylim(0, 110)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, 'student_comparison.png')
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  Chart saved: {path}")

    def grade_distribution(self):
        """Box plot of grade distribution per subject."""
        subjects = DataManager.SUBJECTS
        data = []
        for sub in subjects:
            marks = [s.grades.get(sub, 0) for s in self.dm.students.values() if s.grades]
            data.append(marks if marks else [0])

        fig, ax = plt.subplots(figsize=(10, 6))
        bp = ax.boxplot(data, labels=subjects, patch_artist=True)
        colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_title('Grade Distribution by Subject', fontsize=16, fontweight='bold')
        ax.set_ylabel('Marks')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, 'grade_distribution.png')
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  Chart saved: {path}")

    def eca_impact_analysis(self):
        """Scatter plot: number of ECA activities vs average grade."""
        students = list(self.dm.students.values())
        if not students:
            print("  No students found.")
            return

        eca_counts = [len(s.eca) for s in students]
        avg_grades = [s.average_grade() for s in students]
        names = [s.name for s in students]

        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(eca_counts, avg_grades, c=avg_grades, cmap='RdYlGn',
                             s=150, edgecolor='black', linewidth=0.5, zorder=5)
        for i, name in enumerate(names):
            ax.annotate(name, (eca_counts[i], avg_grades[i]),
                        textcoords="offset points", xytext=(8, 5), fontsize=8)

        # Trend line
        if len(eca_counts) > 1:
            z = np.polyfit(eca_counts, avg_grades, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(eca_counts), max(eca_counts), 100)
            ax.plot(x_line, p(x_line), '--', color='gray', alpha=0.7, label='Trend')
            ax.legend()

        ax.set_title('ECA Impact on Academic Performance', fontsize=16, fontweight='bold')
        ax.set_xlabel('Number of ECA Activities')
        ax.set_ylabel('Average Grade')
        ax.grid(alpha=0.3)
        plt.colorbar(scatter, label='Avg Grade')
        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, 'eca_impact.png')
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"  Chart saved: {path}")

    def performance_alerts(self):
        """Identify students below a threshold."""
        try:
            threshold = float(input("  Enter passing threshold (default 40): ").strip() or "40")
        except ValueError:
            threshold = 40

        print(f"\n  Students with average below {threshold}:")
        print("  " + "-" * 50)
        found = False
        for uid, student in self.dm.students.items():
            avg = student.average_grade()
            if avg < threshold:
                found = True
                print(f"  {student.name} ({uid}) - Average: {avg:.2f}")
                weak = [sub for sub, m in student.grades.items() if m < threshold]
                if weak:
                    print(f"    Weak subjects: {', '.join(weak)}")
                    print(f"    Suggestion: Extra tutoring in {weak[0]}")
        if not found:
            print("  All students are above the threshold.")

    def top_performers(self):
        """Rank students by average grade."""
        students = list(self.dm.students.values())
        ranked = sorted(students, key=lambda s: s.average_grade(), reverse=True)

        print("\n  TOP PERFORMERS RANKING")
        print("  " + "-" * 45)
        print(f"  {'Rank':<6}{'Name':<20}{'Average':>8}")
        print("  " + "-" * 45)
        for i, s in enumerate(ranked, 1):
            avg = s.average_grade()
            medal = ""
            if i == 1: medal = " 🥇"
            elif i == 2: medal = " 🥈"
            elif i == 3: medal = " 🥉"
            print(f"  {i:<6}{s.name:<20}{avg:>8.2f}{medal}")


# ============================================================
# MENU SYSTEM
# ============================================================
class MenuSystem:
    """Handles all menu interactions."""

    def __init__(self):
        self.dm = DataManager()
        self.dm.load_all()
        self.analytics = AnalyticsEngine(self.dm)
        self.current_user = None
        self.current_role = None

    def run(self):
        """Main application loop."""
        print("\n" + "=" * 55)
        print("  STUDENT PROFILE MANAGEMENT SYSTEM")
        print("  Fundamentals of Data Science | UFCFK1-15-0")
        print("=" * 55)

        while True:
            if not self.login():
                continue
            if self.current_role == 'admin':
                self.admin_menu()
            elif self.current_role == 'student':
                self.student_menu()

    # --- Login ---
    def login(self):
        print("\n" + "-" * 40)
        print("  LOGIN")
        print("-" * 40)
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()

        role, user = self.dm.authenticate(username, password)
        if role:
            self.current_role = role
            self.current_user = user
            print(f"\n  Welcome, {user.name}! (Role: {role.upper()})")
            return True
        else:
            print("  [Error] Invalid username or password. Try again.")
            return False

    # --- Admin Menu ---
    def admin_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("  ADMIN MENU")
            print("=" * 50)
            print("  1. View All Students")
            print("  2. Add New Student")
            print("  3. Update Student Record")
            print("  4. Delete Student")
            print("  5. View Student Grades")
            print("  6. Update Student Grades")
            print("  7. View Student ECA")
            print("  8. Update Student ECA")
            print("  9. Analytics Dashboard")
            print("  10. Logout")
            print("-" * 50)

            choice = input("  Enter choice: ").strip()

            if choice == '1':
                self.view_all_students()
            elif choice == '2':
                self.add_student()
            elif choice == '3':
                self.update_student()
            elif choice == '4':
                self.delete_student()
            elif choice == '5':
                self.view_student_grades()
            elif choice == '6':
                self.update_student_grades()
            elif choice == '7':
                self.view_student_eca()
            elif choice == '8':
                self.update_student_eca()
            elif choice == '9':
                self.analytics.show_menu()
            elif choice == '10':
                print("  Logged out.")
                self.dm.save_all()
                break
            else:
                print("  Invalid choice.")

    # --- Student Menu ---
    def student_menu(self):
        student = self.current_user
        while True:
            print("\n" + "=" * 50)
            print(f"  STUDENT MENU - {student.name}")
            print("=" * 50)
            print("  1. View My Profile")
            print("  2. Update My Profile")
            print("  3. View My Grades")
            print("  4. View My ECA")
            print("  5. Logout")
            print("-" * 50)

            choice = input("  Enter choice: ").strip()

            if choice == '1':
                print("\n  --- My Profile ---")
                student.display_info()
            elif choice == '2':
                self.update_own_profile(student)
            elif choice == '3':
                print("\n  --- My Grades ---")
                student.display_grades()
                print(f"\n  Overall Average: {student.average_grade():.2f}")
            elif choice == '4':
                print("\n  --- My ECA ---")
                student.display_eca()
            elif choice == '5':
                print("  Logged out.")
                self.dm.save_all()
                break
            else:
                print("  Invalid choice.")

    # --- Admin Operations ---
    def _select_student(self):
        uid = input("  Enter Student ID: ").strip()
        if uid in self.dm.students:
            return self.dm.students[uid]
        print(f"  [Error] Student '{uid}' not found.")
        return None

    def view_all_students(self):
        print("\n  --- All Students ---")
        if not self.dm.students:
            print("  No students registered.")
            return
        print(f"  {'ID':<8}{'Name':<20}{'Age':<6}{'Average':>8}")
        print("  " + "-" * 45)
        for uid, s in self.dm.students.items():
            print(f"  {uid:<8}{s.name:<20}{s.age:<6}{s.average_grade():>8.2f}")

    def add_student(self):
        print("\n  --- Add New Student ---")
        uid = self.dm.generate_student_id()
        print(f"  Generated ID: {uid}")
        try:
            name = input("  Name: ").strip()
            age = int(input("  Age: ").strip())
            address = input("  Address: ").strip()
            phone = input("  Phone: ").strip()
            password = input("  Set Password: ").strip()

            student = Student(uid, name, age, address, phone)

            # Enter grades
            grades = {}
            print("  Enter grades for each subject (0-100):")
            for sub in DataManager.SUBJECTS:
                while True:
                    try:
                        mark = float(input(f"    {sub}: ").strip())
                        if 0 <= mark <= 100:
                            grades[sub] = mark
                            break
                        else:
                            print("    Enter a value between 0 and 100.")
                    except ValueError:
                        print("    Invalid input. Enter a number.")
            student.grades = grades

            # Enter ECA
            eca_input = input("  ECA activities (semicolon-separated, or leave blank): ").strip()
            if eca_input:
                student.eca = [a.strip() for a in eca_input.split(';') if a.strip()]

            self.dm.students[uid] = student
            self.dm.passwords[uid] = password
            self.dm.save_all()
            print(f"  Student {name} ({uid}) added successfully!")

        except ValueError as e:
            print(f"  [Error] Invalid input: {e}")
        except Exception as e:
            print(f"  [Error] {e}")

    def update_student(self):
        student = self._select_student()
        if not student:
            return
        print(f"\n  Updating: {student.name}")
        name = input(f"  Name [{student.name}]: ").strip()
        age = input(f"  Age [{student.age}]: ").strip()
        address = input(f"  Address [{student.address}]: ").strip()
        phone = input(f"  Phone [{student.phone}]: ").strip()

        if name: student.name = name
        if age:
            try:
                student.age = int(age)
            except ValueError:
                print("  Invalid age, keeping old value.")
        if address: student.address = address
        if phone: student.phone = phone

        self.dm.save_all()
        print("  Student record updated!")

    def delete_student(self):
        student = self._select_student()
        if not student:
            return
        confirm = input(f"  Delete {student.name} ({student.user_id})? (y/n): ").strip().lower()
        if confirm == 'y':
            uid = student.user_id
            del self.dm.students[uid]
            if uid in self.dm.passwords:
                del self.dm.passwords[uid]
            self.dm.save_all()
            print("  Student deleted.")
        else:
            print("  Cancelled.")

    def view_student_grades(self):
        student = self._select_student()
        if student:
            print(f"\n  --- Grades for {student.name} ---")
            student.display_grades()

    def update_student_grades(self):
        student = self._select_student()
        if not student:
            return
        print(f"  Updating grades for {student.name}:")
        for sub in DataManager.SUBJECTS:
            current = student.grades.get(sub, 0)
            val = input(f"    {sub} [{current}]: ").strip()
            if val:
                try:
                    mark = float(val)
                    if 0 <= mark <= 100:
                        student.grades[sub] = mark
                    else:
                        print("    Out of range, keeping old value.")
                except ValueError:
                    print("    Invalid, keeping old value.")
        self.dm.save_all()
        print("  Grades updated!")

    def view_student_eca(self):
        student = self._select_student()
        if student:
            print(f"\n  --- ECA for {student.name} ---")
            student.display_eca()

    def update_student_eca(self):
        student = self._select_student()
        if not student:
            return
        print(f"  Current ECA: {'; '.join(student.eca) if student.eca else 'None'}")
        eca_input = input("  New ECA (semicolon-separated): ").strip()
        if eca_input:
            student.eca = [a.strip() for a in eca_input.split(';') if a.strip()]
            self.dm.save_all()
            print("  ECA updated!")

    def update_own_profile(self, student):
        print("\n  --- Update My Profile ---")
        name = input(f"  Name [{student.name}]: ").strip()
        age = input(f"  Age [{student.age}]: ").strip()
        address = input(f"  Address [{student.address}]: ").strip()
        phone = input(f"  Phone [{student.phone}]: ").strip()

        if name: student.name = name
        if age:
            try:
                student.age = int(age)
            except ValueError:
                print("  Invalid age.")
        if address: student.address = address
        if phone: student.phone = phone

        self.dm.save_all()
        print("  Profile updated!")


# ============================================================
# MAIN ENTRY POINT
# ============================================================
if __name__ == "__main__":
    try:
        app = MenuSystem()
        app.run()
    except KeyboardInterrupt:
        print("\n\n  Program terminated. Goodbye!")
        sys.exit(0)
