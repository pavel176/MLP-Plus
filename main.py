import sys
import log
import soursescript
import compiler
import areaofvisibility

if len(sys.argv) != 2:
	log.help()
	exit()

sourse_script = soursescript.get_sourse_script(sys.argv[1])
log.log_script(sourse_script)

root_aov = areaofvisibility.AOV(end=len(sourse_script)-1)
areaofvisibility.generate_aov(sourse_script, root_aov)
log.log_aov(root_aov)


