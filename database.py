from supabase import create_client, Client

SUPABASE_URL = "https://vtxfuhvnhfhkwapzlnlg.supabase.co"  
SUPABASE_KEY = " "  # Replace with your anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
