from supabase import create_client, Client

SUPABASE_URL = "https://vtxfuhvnhfhkwapzlnlg.supabase.co"  
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ0eGZ1aHZuaGZoa3dhcHpsbmxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM2MDczODgsImV4cCI6MjA1OTE4MzM4OH0.LBrJ7WRMjN2bfIr2UgME0tQm0AZKNUATDVSZSm_9KuE"  # Replace with your anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)