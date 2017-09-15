import App.read_GWAS as reader
import App.unify_columns as unifier
import App.check_correct as checker
import App.rs_liftover


log_file = open("log.txt", 'a')

def main():

    file, df_buffer = reader.init_reader(log_file)
    df_buffer = unifier.init_unify_columns(file, df_buffer)
    #checker.init_check_correct(file, df_buffer)
    
    log_file.close()
