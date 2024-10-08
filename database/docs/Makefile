#
# Copyright 2019 Xilinx, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

.PHONY: all install xml rst html clean cleanhtml cleanall check_tools

all: .stamp/sphinx

check_tools:
ifeq (, $(shell which doxygen 2>/dev/null))
	@echo "ERROR: No doxygen in PATH" && false
endif
ifeq (, $(shell which doxyrest 2>/dev/null))
	@echo "ERROR: No doxyrest in PATH" && false
endif
ifeq (, $(shell which sphinx-build 2>/dev/null))
	@echo "ERROR: No sphinx-build in PATH" && false
endif

install: .stamp/sphinx
ifeq (, $(HTML_DEST_DIR))
	@echo "ERROR: HTML_DEST_DIR is not set." && false
endif
	rsync -av --delete --exclude .git --exclude .nojekyll --exclude .buildinfo \
		 build/html/ $(HTML_DEST_DIR) 1>/dev/null

.stamp/doxygen: | check_tools
	rm -rf xml xml_2 xml_3
	doxygen Doxyfile
	doxygen Doxyfile.2
	doxygen Doxyfile.3
	mkdir -p .stamp
	touch .stamp/doxygen

DOXYREST_FRAME = $(dir $(shell which doxyrest))/../doxyrest_frame

.stamp/doxyrest: .stamp/doxygen | check_tools
	rm -rf src/rst src/rst_2 src/rst_3
	mkdir src/rst src/rst_2 src/rst_3
	doxyrest xml/index.xml -o src/rst/index.rst \
		-F $(DOXYREST_FRAME) -f c_index.rst.in -Dg_verbatimToCodeBlock
	doxyrest xml_2/index.xml -o src/rst_2/index.rst \
		-F $(DOXYREST_FRAME) -f c_index.rst.in -Dg_verbatimToCodeBlock
	doxyrest xml_3/index.xml -o src/rst_3/index.rst \
		-F $(DOXYREST_FRAME) -f c_index.rst.in -Dg_verbatimToCodeBlock
	touch .stamp/doxyrest

.stamp/sphinx: .stamp/doxyrest Makefile.sphinx | check_tools
	make -f Makefile.sphinx html
	touch .stamp/sphinx

xml:
	rm -f .stamp/doxygen
	make .stamp/doxygen

rst:
	rm -f .stamp/doxyrest
	make .stamp/doxyrest

html:
	rm -rf .stamp/sphinx build/doctrees build/html
	make .stamp/sphinx

clean:
	rm -rf .stamp

cleanhtml:
	rm -rf .stamp/sphinx build/html build/doctrees

cleanall:
	rm -rf .stamp xml xml_2 xml_3 build src/rst src/rst_2 src/rst_3
