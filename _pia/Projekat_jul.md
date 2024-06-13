# Project for the Course "Programming Internet Applications (SI)" for the July Exam Period of the 2023/24 School Year

## University of Belgrade, School of Electrical Engineering

### Department of Computer Engineering and Informatics

---

## Project Description

Implement a web system "Good Food Corner" that serves as a platform for booking tables in restaurants and ordering food. There are three types of users: restaurant guest, waiter, and web system administrator.

### User Authentication

All users should be able to log into the system using their credentials (username and password). After entering the correct data, the user can proceed with the rest of the system. In case of incorrect data entry, display an appropriate message.

Restaurant guests and waiters log into the system via a publicly visible form. The system administrator should have the ability to log in via another form, which is not publicly visible (access to the administrator login form should be on a separate route/path, compared to the initial login form for restaurant guests/waiters).

### New User Registration

New users from the restaurant guest category can register by entering the following data:

- Username (unique across all users in the system)
- Password1
- Security question and answer (in case of forgotten password)
- First name
- Last name
- Gender (option: M or F)
- Address
- Contact phone
- Email address (unique, at most one user account per email address)
- Profile picture (added as a file)
- Credit card number

If the data is entered correctly (perform basic checks using JavaScript technology), a new registration request should be created, which must wait for administrator approval before the guest becomes an active system user. The administrator is responsible for reviewing incoming requests, and the outcome can be acceptance or rejection of the registration request. Waiters are added by the administrator. It is not necessary to implement the registration of a new administrator.

During registration, restaurant guests send their profile picture (minimum size 100x100 px, maximum size 300x300 px, in JPG/PNG format); images in the application must be uploaded via the FileUpload window, and manually entered images or those entered via an external link to an image on another site are not acceptable. If no profile picture is added, the guest receives a default profile picture, which already exists in the system.

1 Password should be checked using a regular expression (minimum 6 characters, maximum 10 characters, with at least one uppercase letter, three lowercase letters, one number, and one special character, and must start with a letter). Passwords in the database must be stored encrypted!

### Password Change

All types of users should be allowed to access the password change form on an externally visible page. In the first variant, if the user knows the old password, they enter it and must enter the new password and the repeated new password (in two separate text fields). If the old password is incorrect or the new password is not in the required format, an appropriate message should be displayed. In the second variant, if the user does not know the old password, they enter their username, after which they receive their security question in the second step, to which they must enter the textual answer. If the answer is correct, in the third step they receive a form to enter the new password and the repeated new password (in two separate text fields). Here too, the new password must be in the required format. Once the password is successfully changed, return the user to the initial login screen.

### Unregistered User - Home Page

The home page of the application should display general information about the total number of restaurants, the total number of registered guests in the system, the number of reservations in the last 24 hours, seven days, and a month, and display a list of restaurants with a list of currently engaged waiters (display only their first and last names) in each of those restaurants. Allow sorting (both ascending and descending) of restaurants by each column (name, address, type of restaurant) and allow searching for restaurants by name, address, and/or type of restaurant (not all search fields need to be filled in). Types of restaurants can be Chinese, Indian, Japanese, domestic cuisine, etc.

## Restaurant Guest

After successfully logging into the system, the guest has a main menu consisting of the items described below.

### Profile

The first item in the main menu is "Profile," and this is the page that should be displayed first after logging into the system. Within the profile, the guest can see their basic data (first name, last name, address, email address, contact phone, and credit card number) and can update them. It is also necessary to allow updating the profile picture.

### Restaurants

The second item in the main menu is "Restaurants." Within this item, the guest sees a tabular display of restaurants at the top of the page, just like the unregistered user. All search functionalities available to the unregistered user should be enabled here as well, with the addition that the average rating of the restaurant should be displayed in the results (display the numerical value of the rating, but also visually through star ratings). Additionally, in the tabular display of all restaurants or search results, the user can click on the restaurant's name, which is a link, after which a page with detailed information about that restaurant will be displayed (besides the name, address, and type of restaurant, additionally display the phone number, a list of all comments, and a map with the location, where the map must be functional and dynamic, a static map image is not sufficient).

### Reservations

On the same page with restaurant details, the guest can make a table reservation. The first way to make a reservation is through a form where the user enters the date and time (via Date & Time Picker), the number of people for whom the reservation is made, and a short description (textarea) where the user can enter any additional requirements. Validate the entered reservation and display an appropriate and detailed message to the guest (if the restaurant is closed on that day, or there is no available table in that period for that number of people).

The second way to make a reservation is through an interactive panel (Figure 1), where the guest first enters the exact day and time they want to make the reservation, and then the table occupancy schedule for the selected period is displayed. Tables are drawn on a Canvas graphic element, and a table colored red is an occupied table, while tables that are white are free. Each free table shows the maximum number of people that can sit at that table. By selecting the desired table, it turns green, after which the guest can confirm the reservation by entering the exact number of guests at the table. Canceling the desired table is done by clicking on an empty space on the Canvas element. A reservation cannot be made if a table is not selected. The default duration of guests' stay in the restaurant is 3 hours. A guest can reserve one table per reservation.

![Interactive Panel Example](path_to_image)

### Food Delivery

Apart from the ability to make a reservation at the restaurant, the guest can review the restaurant's menu (each dish has a name, picture, price, and listed ingredients) and order dishes for delivery to the home address. Next to each dish, the user can select the desired quantity and add it to the cart. At any time, the guest can review the cart, modify its contents, and complete the order.

### Reservations Archive

The third item in the main menu is "Reservations." Within this item, the guest sees in the first table all their current reservations, and in the second table all expired reservations. The reservation archive displays reservations from the most recent to the oldest, including the reservation date, restaurant, and optional comment and rating after visiting the restaurant. For each expired reservation that does not have a comment and rating, the guest has a button where a form with a text area for a free comment and a rating from 1 to 5 (using some visual method, e.g., stars that can be clicked) is opened. The guest can leave a rating and comment only for those reservations for which they appeared at the restaurant.

For the table with current reservations, the guest sees the reservation date (with the start time/required arrival time at the restaurant), the name, and the address of the restaurant. In an interval of 45 minutes or more before the start of the reservation, the guest can cancel the reservation.

### Food Delivery Archive

The fourth item in the main menu is "Food Delivery." Here, the guest is shown all current deliveries (display the restaurant name, order status, and estimated delivery time (only after the order is confirmed by the restaurant – described in the waiter section)), as well as all previous deliveries. The delivery archive displays deliveries from the most recent to the oldest, including the delivery date, bill amount, and restaurant.

## Waiter

After successfully logging into the system, the waiter has a main menu consisting of the items described below.

### Profile

The first item in the main menu is "Profile," and this is the page that should be displayed first after logging into the system. Within the profile, the waiter can see their basic data - first name, last name, address, email address, contact phone, and can update all their data. It is also necessary to allow updating the profile picture.

### Reservations

The second item in the main menu is "Reservations." Within this item, the waiter sees all unprocessed reservations for that restaurant, sorted from the most recent to the oldest. Next to each unprocessed reservation, the waiter sees a button and can either confirm or reject it (with a mandatory comment for the rejection). If the reservation was made through the interactive panel, the waiter sees the table chosen by the guest on the panel with the table layout, colored yellow, and upon confirmation of the reservation, the table becomes occupied and red. If the reservation is rejected, the table turns white

 again.

### Food Delivery_

The third item in the main menu is "Food Delivery." Within this item, the waiter sees all unprocessed food orders for that restaurant, sorted from the most recent to the oldest. Next to each order, the waiter sees a button to confirm or reject it (with a mandatory comment for the rejection). The order cannot be modified.

### Current Orders

The fourth item in the main menu is "Current Orders." Within this item, the waiter sees all current food orders that are confirmed, sorted from the most recent to the oldest. Next to each order, the waiter sees the expected delivery time (set by the waiter) and the delivery address. The waiter can also update the delivery status to "Delivered."

## Administrator

After successfully logging into the system, the administrator has a main menu consisting of the items described below.

### Profile_

The first item in the main menu is "Profile," and this is the page that should be displayed first after logging into the system. Within the profile, the administrator can see their basic data - first name, last name, address, email address, contact phone, and can update all their data. It is also necessary to allow updating the profile picture.

### User Management

The second item in the main menu is "User Management." Within this item, the administrator can see all users in the system, their details, and can modify their data. The administrator can also delete users from the system and approve or reject new user registration requests.

### Restaurant Management

The third item in the main menu is "Restaurant Management." Within this item, the administrator can see all restaurants in the system, their details, and can modify their data. The administrator can also add new restaurants to the system and delete existing ones.

### Waiter Management

The fourth item in the main menu is "Waiter Management." Within this item, the administrator can see all waiters in the system, their details, and can modify their data. The administrator can also add new waiters to the system and delete existing ones.

### Reports

The fifth item in the main menu is "Reports." Within this item, the administrator can generate various reports about the system usage, including the number of reservations, the number of food deliveries, and user activity.

### System Settings

The sixth item in the main menu is "System Settings." Within this item, the administrator can configure various system settings, including email notifications, security settings, and other system preferences.

---

### Note

This project should be implemented using appropriate web technologies, ensuring the usability and accessibility of the application.

---

**Prepared by:**

- University of Belgrade, School of Electrical Engineering
- Department of Computer Engineering and Informatics
- Academic Year: 2023/24

---