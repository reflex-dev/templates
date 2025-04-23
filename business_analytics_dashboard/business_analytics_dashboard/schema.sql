
CREATE TABLE employees (
	employee_id SERIAL NOT NULL, 
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	department VARCHAR(50) NOT NULL, 
	CONSTRAINT employees_pkey PRIMARY KEY (employee_id), 
	CONSTRAINT employees_email_key UNIQUE (email)
)



CREATE TABLE expense_categories (
	category_id SERIAL NOT NULL, 
	category_name VARCHAR(100) NOT NULL, 
	description TEXT, 
	CONSTRAINT expense_categories_pkey PRIMARY KEY (category_id)
)



CREATE TABLE expense_reports (
	report_id SERIAL NOT NULL, 
	employee_id INTEGER NOT NULL, 
	report_month DATE NOT NULL, 
	total_amount NUMERIC(10, 2) DEFAULT 0 NOT NULL, 
	submission_date DATE NOT NULL, 
	approval_status VARCHAR(20) NOT NULL, 
	CONSTRAINT expense_reports_pkey PRIMARY KEY (report_id), 
	CONSTRAINT expense_reports_employee_id_fkey FOREIGN KEY(employee_id) REFERENCES employees (employee_id)
)



CREATE TABLE expenses (
	expense_id SERIAL NOT NULL, 
	report_id INTEGER NOT NULL, 
	expense_date DATE NOT NULL, 
	category_id INTEGER NOT NULL, 
	amount NUMERIC(10, 2) NOT NULL, 
	description TEXT, 
	receipt_url TEXT, 
	CONSTRAINT expenses_pkey PRIMARY KEY (expense_id), 
	CONSTRAINT expenses_category_id_fkey FOREIGN KEY(category_id) REFERENCES expense_categories (category_id), 
	CONSTRAINT expenses_report_id_fkey FOREIGN KEY(report_id) REFERENCES expense_reports (report_id)
)


