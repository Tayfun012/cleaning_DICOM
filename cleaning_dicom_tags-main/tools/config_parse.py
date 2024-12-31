
class Config_parse:

    def parse_config_remove_tag(DICOM_TAGS, remove_tags,config):
        remove_tags_list=list()
        if config.has_option(DICOM_TAGS, remove_tags):
            tags_list = config.get(DICOM_TAGS, remove_tags)
            tags_list = [tuple(map(lambda x: int(x.replace('(0x', '').replace(')', ''), 16), x.split(','))) for x in tags_list.split('), ')]
            remove_tags_list = [(int(x[0]), int(x[1])) for x in tags_list]
        else: 
            remove_tags_list=[]
        return remove_tags_list
    

    def parse_config_remove_string(DICOM_TAGS,selection,config):
        selection_list=list()
        if config.has_option(DICOM_TAGS, selection):    
            selection_list  = config.get(DICOM_TAGS, selection)
            selection_list = selection_list.split(",")
            selection_list = [elem.strip("'") for elem in selection_list]
        else:
            selection_list=[]
        return selection_list