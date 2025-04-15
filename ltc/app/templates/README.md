# Templates README

StaDocGen templates are structured into a core set comprised of a shared global template and a separate template for each page, which is further divided into  parts that define the major structural components of a given page. Each page has a unique set of components and a global set shared by all pages.

Templates (includes) in the language subdirectories override the includes in the root directory. If a specific includes doesn't exist in a language, the site falls back to the 
file in the default includes directory.

/
	- Page templates and the shared base template
/icludes
	- Default set of includes	
/[language tag]/includes
	- Include templates translated into the language specified by the [language tag]. The contents
	of this directory override the contents in the default includes foler
	
	
