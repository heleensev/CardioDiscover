import App.global_class as glob
import App.read_GWAS as reader
import App.identify_columns as column_IDer
import App.check_correct as checker
import App.rs_liftover

log = glob.LogFile()

def main():

    file, filename = reader.init_reader()
    #do something with headers, write to df or something
    headers = column_IDer.init_column_IDer(file)
    df = checker.init_check_correct(file)

    log.close()