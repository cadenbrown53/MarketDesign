import random
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define the market parameters
num_students = 18
num_schools = 3
school_capacity = 6

# Create sets of students and schools
students = [f"i{i+1}" for i in range(num_students)]
schools = [f"s{i+1}" for i in range(num_schools)]

print(f"Students: {students}")
print(f"Schools: {schools}")
print(f"School capacity: {school_capacity}")
print()

# 1. Generate Student Preferences
# For each student, generate a strict random preference ranking over all schools
student_preferences = {}
for student in students:
    # Randomly shuffle the schools to create a preference ranking
    pref = schools.copy()
    random.shuffle(pref)
    student_preferences[student] = pref

print("Student Preferences:")
for student, prefs in student_preferences.items():
    print(f"  {student}: {' > '.join(prefs)}")
print()

# 2. Generate School Priorities
# For each school, generate a strict random priority ordering over all students
school_priorities = {}
for school in schools:
    # Randomly shuffle the students to create a priority ordering
    priority = students.copy()
    random.shuffle(priority)
    school_priorities[school] = priority

print("School Priorities:")
for school, priorities in school_priorities.items():
    print(f"  {school}: {' > '.join(priorities)}")
print()

# Save output to a markdown file for easy viewing
with open('problem_set_02/market_setup_output.md', 'w') as f:
    f.write("# School Choice Market Setup\n\n")
    f.write(f"**Number of Students:** {num_students}\n\n")
    f.write(f"**Number of Schools:** {num_schools}\n\n")
    f.write(f"**School Capacity:** {school_capacity}\n\n")
    
    f.write("## Students\n")
    f.write(", ".join(students) + "\n\n")
    
    f.write("## Schools\n")
    f.write(", ".join(schools) + "\n\n")
    
    f.write("## Student Preferences\n\n")
    f.write("Each student's preference ranking over schools (most preferred to least preferred):\n\n")
    for student, prefs in student_preferences.items():
        f.write(f"- **{student}**: {' > '.join(prefs)}\n")
    
    f.write("\n## School Priorities\n\n")
    f.write("Each school's priority ordering over students (highest priority to lowest priority):\n\n")
    for school, priorities in school_priorities.items():
        f.write(f"- **{school}**: {' > '.join(priorities)}\n")

print("✓ Output saved to problem_set_02/market_setup_output.md")
