IMAGES_SRC=$(wildcard images/*.png)
IMAGES_TARGET=$(patsubst images%,UserGuide/html/images%,$(IMAGES_SRC))
USERGUIDE_FOLDER=UserGuide
PROGGUIDE_FOLDER=ProgrammerGuide

default: install

$(USERGUIDE_FOLDER)/html $(USERGUIDE_FOLDER)/html/images :
	mkdir -p $@

$(USERGUIDE_FOLDER)/html/images/%.png : images/%.png
	cp $< $@


$(USERGUIDE_FOLDER)/html/t1.html:  $(USERGUIDE_FOLDER)/html UserGuide.xml 
	docbook2html -o $(USERGUIDE_FOLDER)/html UserGuide.xml

$(PROGGUIDE_FOLDER)/html/index.html: ProgrammerGuide.cfg
	doxygen $<

install docs: $(PROGGUIDE_FOLDER)/html/index.html $(USERGUIDE_FOLDER)/html/t1.html  $(USERGUIDE_FOLDER)/html $(USERGUIDE_FOLDER)/html/images $(IMAGES_TARGET)

uninstall clean:
	-if test -e $(PROGGUIDE_FOLDER);  then rm -r $(PROGGUIDE_FOLDER); fi
	-if test -e $(USERGUIDE_FOLDER);  then rm -r $(USERGUIDE_FOLDER); fi
