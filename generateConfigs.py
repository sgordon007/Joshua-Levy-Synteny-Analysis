def generateConfigs(configPath,KaryotypePath,LinkPath,KaryotypeFiles,linkFile,subgenomesCheck):
    configText = """# circos.conf
    # 240:circos-0.69 jlevy$ /Applications/circos-0.69/bin/circos -conf /Applications/circos-0.69/bin/circos.conf

    karyotype = %s,%s

    chromosomes_units = 1000000
    #chromosomes_scale = /./=1rn
    chromosomes_display_default = yes

    # include ideogram configuration
    <<include %stxideogram.conf>>

    ## include ticks configuration
    <<include %stxticks.conf>>

    <colors>
    </colors>

    # include links and rules
    <<include %slinksAndrules.conf>>



    ################################################################
    # The remaining content is standard and required. It is imported
    # from default files in the Circos distribution.
    #
    # These should be present in every Circos configuration file and
    # overridden as required. To see the content of these files,
    # look in etc/ in the Circos distribution.

    <image>
    # Included from Circos distribution.
    <<include etc/image.conf>>
    </image>

    # RGB/HSV color definitions, color lists, location of fonts, fill patterns.
    # Included from Circos distribution.
    <<include etc/colors_fonts_patterns.conf>>

    # Debugging, I/O an dother system parameters
    # Included from Circos distribution.
    <<include etc/housekeeping.conf>>"""%(KaryotypePath+KaryotypeFiles[0],KaryotypePath+KaryotypeFiles[1],configPath,
                                          configPath,configPath)

    linkAndruleChunk1 = """# links and rules

    <links>

    <link>
    file = %s
    radius = 0.99r
    bezier_radius = 0r
    #thickness = 2
    ribbon = yes
    color = black_a4

    <rules>
    <rule>
    condition = var(intrachr)
    show = no
    </rule>

    """%(LinkPath+linkFile)

    # let's make  linkAndruleChunk2
    # looks like...
    """<rule>
    condition = to(ChrSy)
    color = chr14
    </rule>"""
    ruleInputFile = open(KaryotypePath+KaryotypeFiles[1],'r')
    ruleList = []
    if subgenomesCheck:
        count = 1
        for line in ruleInputFile:
            ruleList += ['\n<rule>\ncondition = to(%s)\ncolor = chr%d\n</rule>\n' % (line.split()[2],count)]
            count += 1
    else:
        for line in ruleInputFile:
            lineList = line.split()
            ruleList += ['\n<rule>\ncondition = to(%s)\ncolor = %s\n</rule>\n'%(lineList[2],lineList[-1])]
    ruleInputFile.close()
    linkAndruleChunk2 = ''.join(str(rule) for rule in ruleList)


    linkAndruleChunk3 = """

    </rules>
    </link>


    </links>"""

    linkAndruleConfigOut = linkAndruleChunk1+linkAndruleChunk2+linkAndruleChunk3

    # generate Config Files circos and linksandrules
    open(configPath+'circos.conf','w').close()
    open(configPath+'linksAndrules.conf','w').close()

    circosConfig = open(configPath+'circos.conf','w')
    circosConfig.write(configText)
    circosConfig.close()

    linksAndRuleConfig = open(configPath+'linksAndrules.conf','w')
    linksAndRuleConfig.write(linkAndruleConfigOut)
    linksAndRuleConfig.close()