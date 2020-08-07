
import re

def oxford_parser_shit(response):
    definition_dict = {}

    # Each type of meaning [noun, verb...] is in a  <section class="gramb">
    for grammar_word_type_section in response.xpath("//section[@class='gramb']"):
        try:
            # The first <span class="pos">noun</span> contains the type of word
            part_of_speech = grammar_word_type_section.xpath(".//span[@class='pos']/text()").extract()[0]
        except:
            part_of_speech = False

        if part_of_speech:
            definition_dict[part_of_speech] = dict()

        # For each meaning <div class="trg"> 
        for meaning_div in grammar_word_type_section.xpath(".//div[@class='trg']"):
            try:
                # The first <span class="iteration">1 contains the type of word
                meaning_index = meaning_div.xpath(".//span[@class='iteration']/text()").extract()[0]
            except:
                meaning_index = False

            def_list = meaning_div.xpath(".//span[@class='ind']").extract()
            # print (def_list)
            if not def_list:
                def_list = meaning_div.xpath(".//div[@class='empty_sense']//div[@class='crossReference']").extract()
                
            
            def_list = [re.sub(r'<.*?>', "", i).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech and meaning_index:
                def_list= [def_list[0]]
                if meaning_index in definition_dict[part_of_speech]:
                    definition_dict[part_of_speech][meaning_index] += def_list
                else:
                    definition_dict[part_of_speech][meaning_index] = def_list
        
    return definition_dict



def oxford_parser(response):
    definition_dict = {}

    # Each type of meaning [noun, verb...] is in a  <section class="gramb">
    for grammar_word_type_section in response.xpath("//section[@class='gramb']"):
        try:
            # The first <span class="pos">noun</span> contains the type of word
            part_of_speech = grammar_word_type_section.xpath(".//span[@class='pos']/text()").extract()[0]
        except:
            part_of_speech = False

        def_list = grammar_word_type_section.xpath("./ul/li/div[@class='trg']//span[@class='ind']").extract()
        if not def_list:
            def_list = grammar_word_type_section.xpath(".//div[@class='empty_sense']//div[@class='crossReference']").extract()

        def_list = [re.sub(r'<.*?>', "", i).strip() for i in def_list]
        def_list = [i for i in def_list if i]

        if def_list and part_of_speech:
            if part_of_speech in definition_dict:
                definition_dict[part_of_speech] += def_list
            else:
                definition_dict[part_of_speech] = def_list
    
    return definition_dict