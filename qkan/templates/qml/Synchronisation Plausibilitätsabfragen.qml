<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.40.14-Bratislava" styleCategories="LayerConfiguration|Symbology|Forms|AttributeTable|Notes">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <fieldConfiguration>
    <field name="pk">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pk_best">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="pk_ext">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="aktion">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="status">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNullState"/>
            <Option value="1" type="QString" name="CheckedState"/>
            <Option value="1" type="int" name="TextDisplayMethod"/>
            <Option value="0" type="QString" name="UncheckedState"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="gruppe">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="warntext">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="warntyp">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="warnlevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sql">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="layername">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="attrname">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column type="field" width="-1" hidden="0" name="status"/>
      <column type="field" width="-1" hidden="0" name="aktion"/>
      <column type="field" width="-1" hidden="0" name="gruppe"/>
      <column type="field" width="-1" hidden="0" name="warntext"/>
      <column type="field" width="-1" hidden="0" name="warntyp"/>
      <column type="field" width="-1" hidden="0" name="warnlevel"/>
      <column type="field" width="-1" hidden="0" name="sql"/>
      <column type="field" width="-1" hidden="0" name="layername"/>
      <column type="field" width="-1" hidden="0" name="attrname"/>
      <column type="field" width="-1" hidden="0" name="pk"/>
      <column type="field" width="-1" hidden="0" name="pk_best"/>
      <column type="field" width="-1" hidden="0" name="pk_ext"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles>
      <style rule="status and aktion = 'hinzufügen'" background_color="#b2df8a" background_color_alpha="255" name="hinzufügen">
        <font strikethrough="0" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" italic="0"/>
      </style>
      <style rule="not status and aktion = 'hinzufügen'" text_color="#33a02c" text_color_alpha="255" name="hinzufügen nicht ausführen">
        <font strikethrough="1" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,1,0,1,0,0" italic="1"/>
      </style>
      <style rule="status and aktion = 'ändern'" background_color="#fdbf6f" background_color_alpha="255" name="ändern">
        <font strikethrough="0" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" italic="0"/>
      </style>
      <style rule="not status and aktion = 'ändern'" text_color="#ff7f00" text_color_alpha="255" name="ändern nicht ausführen">
        <font strikethrough="1" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.3,-1,5,50,1,0,1,0,0" italic="1"/>
      </style>
      <style rule="status and aktion = 'löschen'" background_color="#fb9a99" background_color_alpha="255" name="löschen">
        <font strikethrough="0" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" italic="0"/>
      </style>
      <style rule="not status and aktion = 'löschen'" text_color="#e31a1c" text_color_alpha="255" name="löschen nicht ausführen">
        <font strikethrough="1" style="" underline="0" bold="0" description="MS Shell Dlg 2,8.3,-1,5,50,1,0,1,0,0" italic="1"/>
      </style>
      <style text_color="#5500ff" name="redundant" rule="aktion = 'Bezeichnung im Bestand nicht eindeutig'" text_color_alpha="255" background_color_alpha="255" background_color="#e6d9ff">
        <font strikethrough="0" italic="1" bold="1" description="MS Shell Dlg 2,8.3,-1,5,75,1,0,0,0,0" underline="0" style=""/>
      </style>
      <style text_color="#9500ff" name="redundant extern" rule="aktion = 'Bezeichnung extern nicht eindeutig'" text_color_alpha="255" background_color_alpha="255" background_color="#efd9ff">
        <font strikethrough="0" italic="1" bold="1" description="MS Shell Dlg 2,8.3,-1,5,75,1,0,0,0,0" underline="0" style=""/>
      </style>
    </rowstyles>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS-Formulare können eine Python-Funktion haben,, die aufgerufen wird, wenn sich das Formular öffnet

Diese Funktion kann verwendet werden um dem Formular Extralogik hinzuzufügen.

Der Name der Funktion wird im Feld "Python Init-Function" angegeben
Ein Beispiel folgt:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <editable>
    <field name="aktion" editable="0"/>
    <field name="attrname" editable="0"/>
    <field name="gruppe" editable="0"/>
    <field name="layername" editable="0"/>
    <field name="pk" editable="0"/>
    <field name="pk_best" editable="0"/>
    <field name="pk_ext" editable="0"/>
    <field name="sql" editable="0"/>
    <field name="status" editable="1"/>
    <field name="warnlevel" editable="0"/>
    <field name="warntext" editable="0"/>
    <field name="warntyp" editable="0"/>
  </editable>
  <labelOnTop>
    <field name="aktion" labelOnTop="0"/>
    <field name="attrname" labelOnTop="0"/>
    <field name="gruppe" labelOnTop="0"/>
    <field name="layername" labelOnTop="0"/>
    <field name="pk" labelOnTop="0"/>
    <field name="pk_best" labelOnTop="0"/>
    <field name="pk_ext" labelOnTop="0"/>
    <field name="sql" labelOnTop="0"/>
    <field name="status" labelOnTop="0"/>
    <field name="warnlevel" labelOnTop="0"/>
    <field name="warntext" labelOnTop="0"/>
    <field name="warntyp" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="aktion"/>
    <field reuseLastValue="0" name="attrname"/>
    <field reuseLastValue="0" name="gruppe"/>
    <field reuseLastValue="0" name="layername"/>
    <field reuseLastValue="0" name="pk"/>
    <field reuseLastValue="0" name="pk_best"/>
    <field reuseLastValue="0" name="pk_ext"/>
    <field reuseLastValue="0" name="sql"/>
    <field reuseLastValue="0" name="status"/>
    <field reuseLastValue="0" name="warnlevel"/>
    <field reuseLastValue="0" name="warntext"/>
    <field reuseLastValue="0" name="warntyp"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"layername"</previewExpression>
  <layerGeometryType>4</layerGeometryType>
</qgis>
