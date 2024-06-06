# Faculty of Electrical Engineering in Belgrade
## Department of Computer Engineering and Informatics
### Data Protection
### Project Assignment 2023/2024

<div align="justify">

## Project Assignment Description
The aim of the project assignment is to better understand the PGP scheme for email protection, as well as the capabilities it offers and how to use it. For this purpose, the task involves designing and implementing an application with a graphical user interface in the Python programming language that should enable the following functionalities:
- Generation of new and deletion of existing RSA key pairs
- Import and export of the public part of the key or the entire key pair in .pem format
- Display of the public and private keyring with all necessary information
- Sending a message (ensuring encryption and signing)
- Receiving a message (ensuring decryption and verification)

When generating a new key pair, the user must enter a name, email, and key size (1024 or 2048 bits). After entering all necessary data, the user must enter a password under which the private key will be stored. All generated and imported keys should be clearly visible in the user interface. Each access to the private key should be secured by requesting the password. Students should propose and implement structures in which the keys are stored (public and private keyring).

When sending a message, the user should be offered the option to encrypt the message to ensure confidentiality, sign the message to ensure authenticity, compress the message, and convert the data to radix-64 format. To ensure authenticity, allow the user to select the private key they want to use for signing the message using SHA-1 to generate the hash function. To ensure confidentiality, allow the user to select the public key used for encrypting the message and the symmetric algorithm. Two (optionally) of the following four proposed algorithms should be supported: TripleDES, AES128, Cast5, and IDEA. Sending the message creates a new file at the desired destination chosen by the user. The file should contain all the necessary information that needs to be delivered to the recipient. The structure of the file should correspond to the structure covered in the exercise classes, and students should propose and implement all the details of storing information in the file.

When receiving a message, the user selects the file from the desired destination, and the application recognizes the packages and performs decryption and verification. After receiving the message, the user is shown information about the success of the signature verification and information about the author of the signature if the appropriate service is used. After that, the user should be allowed to save the original message to the desired destination. In case of unsuccessful decryption or verification, display a clear error message on the user interface.

## Notes:
- The project assignment for the Data Protection course is done in teams of two students. Individual work is also possible, but it is not recommended as it does not bring additional points.
- The project assignment can be defended exclusively in the June or August exam period. The deadline for submission and defense dates will be announced later. If the student defends the project in the August period, the exam can be taken no earlier than the August period (points from the June and July exams are not retained).
- The project assignment is not mandatory and can bring a maximum of 15 or 20 points that cannot be compensated by other pre-exam or exam obligations. Depending on the number of points the project carries, the points from laboratory exercises are scaled to 15 or 10. The distribution of points for the project and laboratory exercises will be automatically determined based on which distribution gives a higher total number of points for each student individually.
- In the oral defense, the candidate must independently run their solution submitted by the deadline. The candidate must possess the necessary level of knowledge about the task, be aware of the shortcomings of the submitted solution, and the ability to resolve these shortcomings. The candidate must correctly answer a certain number of questions related to the assignment topic and successfully implement the modification solution.
- Before starting to solve the problem or seeking help, read the task and the attached documentation in its entirety and carefully. If something in the task is not precisely defined, students are expected to introduce reasonable assumptions.
- When implementing the solution, students are obliged to adhere to the following rules:
  - Students are allowed to take ideas about the message structure and functionality implementation from the standard defined in the RFC 4480 document describing the OpenPGP protocol.
  - Students are allowed to use ready-made modules for implementing parts of the PGP scheme (e.g., rsa module, cryptography module, etc.).
  - Students are not allowed to use ready-made modules that offer ready-made PGP scheme functionalities (e.g., py-pgp module).
  - Students within a team should divide responsibilities into equal parts.
  - It is not allowed for students within a team to divide responsibilities such that one team member works on implementing the application logic, and the other works on implementing the graphical user interface.
  - It is forbidden to take ready-made solutions from the internet and share solutions with other teams. All submitted solutions will be passed through a code similarity checking application. If it is found that two or more submitted solutions have a higher degree of similarity than allowed, all authors will be reported to the Faculty's disciplinary committee.
- Send any questions to the assistants via email, but as one message: teodora@etf.bg.ac.rs, aki@etf.bg.ac.rs, majav@etf.bg.ac.rs

</div>