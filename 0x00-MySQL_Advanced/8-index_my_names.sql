-- Create an index on the first letter of name in the names table
CREATE INDEX idx_name_first ON names (LEFT(name, 1));
