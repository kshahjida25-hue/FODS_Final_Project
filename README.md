# Student Profile Management System
## Fundamentals of Data Science | UFCFK1-15-0 | Final Assessment Project

### Project Structure
```
FODS_Project/
├── main.py                          # Main Python source code
├── sample_data/
│   ├── users.txt                    # User records (admin/student)
│   ├── grades.txt                   # Student grades (5 subjects)
│   ├── eca.txt                      # Extracurricular activities
│   └── passwords.txt                # Login credentials
├── charts/                          # Generated analytics charts
│   ├── subject_averages.png
│   ├── student_comparison.png
│   ├── grade_distribution.png
│   ├── eca_impact.png
│   └── flowchart.png
├── screenshots/
│   └── sample_output.txt            # Sample console output
├── Report_FODS_Project.docx         # Written report
├── Presentation_FODS_Project.pptx   # Presentation slides
└── README.md                        # This file
```

### How to Run
```bash
pip install matplotlib numpy
python main.py
```

### Sample Login Credentials
| Username | Password   | Role    |
|----------|------------|---------|
| A001     | admin123   | Admin   |
| S001     | aarav123   | Student |
| S002     | sita123    | Student |

### Features
- Login system with role-based access (admin/student)
- Admin: Add, update, delete students; manage grades & ECA; analytics dashboard
- Student: View/update profile, view grades & ECA
- OOP design: Inheritance, encapsulation, polymorphism
- File handling with 4 text files
- Exception handling throughout
- Analytics Dashboard with 6 chart types (matplotlib)
