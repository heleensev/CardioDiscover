import App.global_functions as glob
import App.read_GWAS as reader
import App.identify_columns as column_IDer
import App.check_correct as checker
import App.rs_liftover


def main():
    glob.globals()
    file, sep = reader.init_reader(log_file)
    headers = column_IDer.init_header_ider(file, sep)
    df = checker(file, headers)
    #checker.init_check_correct(file, df_buffer)
    
    log_file.close()
