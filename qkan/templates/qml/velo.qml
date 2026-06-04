<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="0" version="3.40.14-Bratislava" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|MapTips|AttributeTable|Rendering|Temporal|Legend|Notes" labelsEnabled="0" minScale="100000000" simplifyDrawingTol="1" readOnly="0" simplifyLocal="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" maxScale="0" autoRefreshMode="Disabled" symbologyReferenceScale="-1" autoRefreshTime="0" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="1" limitMode="0" fixedDuration="0" accumulate="0" durationField="pk" durationUnit="min" startField="" mode="4" startExpression=" to_datetime( tanf)" endField="" endExpression=" to_datetime( tend)">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="graduatedSymbol" forceraster="0" symbollevels="0" attr="v" enableorderby="0" graduatedMethod="GraduatedColor" referencescale="-1">
    <ranges>
      <range uuid="{98eb8b6d-cb27-467a-867e-0be65fcbf6ee}" label="0 - 0.25" symbol="0" render="true" upper="0.250000000000000" lower="0.000000000000000"/>
      <range uuid="{6ead278e-ab22-4099-b790-a163d54dfae7}" label="0.25 - 0.5" symbol="1" render="true" upper="0.500000000000000" lower="0.250000000000000"/>
      <range uuid="{ca30b273-ffb3-4e9e-847b-3851cd0cb383}" label="0.5 - 0.75" symbol="2" render="true" upper="0.750000000000000" lower="0.500000000000000"/>
      <range uuid="{dbac09a1-6426-4983-8c3e-1343f6980021}" label="0.75 - 1" symbol="3" render="true" upper="1.000000000000000" lower="0.750000000000000"/>
      <range uuid="{d7379d29-c0cc-4a4f-b158-234351df77a9}" label="1 - 1.25" symbol="4" render="true" upper="1.250000000000000" lower="1.000000000000000"/>
      <range uuid="{4dbfc923-e54c-498e-9c73-3ce5e9d2966b}" label="1.25 - 1.5" symbol="5" render="true" upper="1.500000000000000" lower="1.250000000000000"/>
      <range uuid="{62a5245b-6f1c-4085-902d-9f7004dfd120}" label="1.5 - 1.75" symbol="6" render="true" upper="1.750000000000000" lower="1.500000000000000"/>
      <range uuid="{953e3bee-69b0-40ea-b8d2-5475d2077ab2}" label="1.75 - 2" symbol="7" render="true" upper="2.000000000000000" lower="1.750000000000000"/>
      <range uuid="{3a77decb-a302-410f-92aa-cbbc231888d5}" label="2 - 2.25" symbol="8" render="true" upper="2.250000000000000" lower="2.000000000000000"/>
      <range uuid="{78259625-05cc-4b39-8a53-ace86cece391}" label="2.25 - 2.5" symbol="9" render="true" upper="2.500000000000000" lower="2.250000000000000"/>
      <range uuid="{c9926257-27b5-4de8-ae10-6f1b5e6bf612}" label="2.5 - 2.75" symbol="10" render="true" upper="2.750000000000000" lower="2.500000000000000"/>
      <range uuid="{a4dbf022-c671-4dfd-84f1-2852b3b0f661}" label="2.75 - 3" symbol="11" render="true" upper="3.000000000000000" lower="2.750000000000000"/>
      <range uuid="{e998623b-4e91-4d17-a89b-8cb69d0eec75}" label="3 - 3.25" symbol="12" render="true" upper="3.250000000000000" lower="3.000000000000000"/>
      <range uuid="{a6792535-ea5b-4bc9-8038-6d3b2de4bc1f}" label="3.25 - 3.5" symbol="13" render="true" upper="3.500000000000000" lower="3.250000000000000"/>
      <range uuid="{45ad6ee5-ee42-4280-975e-cbeacd28fe05}" label="3.5 - 3.75" symbol="14" render="true" upper="3.750000000000000" lower="3.500000000000000"/>
      <range uuid="{ade0fd46-c38c-4a9e-b7ed-b57deba2258a}" label="3.75 - 4" symbol="15" render="true" upper="4.000000000000000" lower="3.750000000000000"/>
      <range uuid="{88ab7837-ac71-42ff-80ce-c9cd9f1cb66b}" label="4 - 4.25" symbol="16" render="true" upper="4.250000000000000" lower="4.000000000000000"/>
      <range uuid="{a901c058-c491-497b-a59f-14c61882e905}" label="4.25 - 4.5" symbol="17" render="true" upper="4.500000000000000" lower="4.250000000000000"/>
      <range uuid="{cb2d47ed-bf94-462b-b2a9-404e662fc813}" label="4.5 - 4.75" symbol="18" render="true" upper="4.750000000000000" lower="4.500000000000000"/>
      <range uuid="{8f14234e-0c9a-4c49-989d-d21d6622c0fe}" label=" > 4.75" symbol="19" render="true" upper="1000.000000000000" lower="4.750000000000000"/>
    </ranges>
    <symbols>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="0" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="48,18,59,255,rgb:0.18823529411764706,0.07058823529411765,0.23137254901960785,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="1" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="62,57,148,255,rgb:0.24499885557335774,0.2251773861295491,0.57976653696498059,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="10" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="182,247,53,255,rgb:0.71454947737850005,0.96966506446936751,0.20888075074387732,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="11" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="215,229,53,255,rgb:0.84478522926680399,0.89721522850385294,0.20866712443732358,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="12" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="240,204,58,255,rgb:0.94262607766842144,0.79855039291981389,0.22745098039215686,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="13" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="253,174,53,255,rgb:0.99215686274509807,0.6811169604028382,0.20721751735713742,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="14" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="252,136,37,255,rgb:0.98968490119783326,0.53374532692454413,0.14654764629587244,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="15" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="242,96,20,255,rgb:0.94860761425192641,0.37523460746166171,0.0780193789578088,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="16" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="224,64,8,255,rgb:0.87780575265125504,0.25035477225909819,0.03302052338445106,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="17" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="197,38,3,255,rgb:0.77213702601663237,0.1488059815365835,0.01176470588235294,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="18" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="162,18,1,255,rgb:0.63694209201190199,0.07244983596551462,0.00392156862745098,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="19" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="122,4,3,255,rgb:0.47843137254901963,0.01568627450980392,0.01176470588235294,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="2" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="69,94,211,255,rgb:0.27058823529411763,0.36821545738918138,0.82662699320973521,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="3" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="70,129,247,255,rgb:0.27450980392156865,0.5052567330434119,0.96800183108262761,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="4" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="58,163,252,255,rgb:0.22786297398336766,0.63797970550087735,0.9886472877088579,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="5" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="35,196,227,255,rgb:0.13580529488059814,0.76758983749141685,0.89123369192034796,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="6" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="24,222,192,255,rgb:0.09411764705882353,0.86996261539635311,0.75417715724422063,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="7" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="45,240,157,255,rgb:0.17625696192874038,0.94241245136186769,0.6158999008163577,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="8" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="92,252,112,255,rgb:0.36140993362325474,0.9874113069352255,0.43859006637674525,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="9" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="144,255,72,255,rgb:0.56388189517051956,1,0.28421454184786754,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="0" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{0ffcac05-7ba5-4021-8eda-4cb1ea8f646d}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="48,18,59,255,rgb:0.18823529411764706,0.07058823529411765,0.23137254901960785,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="arrow" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="angle">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="90.0 - angle" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="v * 2" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <colorramp type="gradient" name="[source]">
      <Option type="Map">
        <Option value="48,18,59,255,rgb:0.18823529411764706,0.07058823529411765,0.23137254901960785,1" type="QString" name="color1"/>
        <Option value="122,4,3,255,rgb:0.47843137254901963,0.01568627450980392,0.01176470588235294,1" type="QString" name="color2"/>
        <Option value="ccw" type="QString" name="direction"/>
        <Option value="0" type="QString" name="discrete"/>
        <Option value="gradient" type="QString" name="rampType"/>
        <Option value="rgb" type="QString" name="spec"/>
        <Option value="0.0039063;50,21,67,255,rgb:0.19607843137254902,0.08235294117647059,0.2627450980392157,1;rgb;ccw:0.0078125;51,24,74,255,rgb:0.20000000000000001,0.09411764705882353,0.29019607843137257,1;rgb;ccw:0.0117188;52,27,81,255,rgb:0.20392156862745098,0.10588235294117647,0.31764705882352939,1;rgb;ccw:0.015625;53,30,88,255,rgb:0.20784313725490197,0.11764705882352941,0.34509803921568627,1;rgb;ccw:0.0195313;54,33,95,255,rgb:0.21176470588235294,0.12941176470588237,0.37254901960784315,1;rgb;ccw:0.0234375;55,36,102,255,rgb:0.21568627450980393,0.14117647058823529,0.40000000000000002,1;rgb;ccw:0.0273438;56,39,109,255,rgb:0.2196078431372549,0.15294117647058825,0.42745098039215684,1;rgb;ccw:0.03125;57,42,115,255,rgb:0.22352941176470589,0.16470588235294117,0.45098039215686275,1;rgb;ccw:0.0351563;58,45,121,255,rgb:0.22745098039215686,0.17647058823529413,0.47450980392156861,1;rgb;ccw:0.0390625;59,47,128,255,rgb:0.23137254901960785,0.18431372549019609,0.50196078431372548,1;rgb;ccw:0.0429688;60,50,134,255,rgb:0.23529411764705882,0.19607843137254902,0.52549019607843139,1;rgb;ccw:0.046875;61,53,139,255,rgb:0.23921568627450981,0.20784313725490197,0.54509803921568623,1;rgb;ccw:0.0507813;62,56,145,255,rgb:0.24313725490196078,0.2196078431372549,0.56862745098039214,1;rgb;ccw:0.0546875;63,59,151,255,rgb:0.24705882352941178,0.23137254901960785,0.59215686274509804,1;rgb;ccw:0.0585938;63,62,156,255,rgb:0.24705882352941178,0.24313725490196078,0.61176470588235299,1;rgb;ccw:0.0625;64,64,162,255,rgb:0.25098039215686274,0.25098039215686274,0.63529411764705879,1;rgb;ccw:0.0664063;65,67,167,255,rgb:0.25490196078431371,0.2627450980392157,0.65490196078431373,1;rgb;ccw:0.0703125;65,70,172,255,rgb:0.25490196078431371,0.27450980392156865,0.67450980392156867,1;rgb;ccw:0.0742188;66,73,177,255,rgb:0.25882352941176473,0.28627450980392155,0.69411764705882351,1;rgb;ccw:0.078125;66,75,181,255,rgb:0.25882352941176473,0.29411764705882354,0.70980392156862748,1;rgb;ccw:0.0820313;67,78,186,255,rgb:0.2627450980392157,0.30588235294117649,0.72941176470588232,1;rgb;ccw:0.0859375;68,81,191,255,rgb:0.26666666666666666,0.31764705882352939,0.74901960784313726,1;rgb;ccw:0.0898438;68,84,195,255,rgb:0.26666666666666666,0.32941176470588235,0.76470588235294112,1;rgb;ccw:0.09375;68,86,199,255,rgb:0.26666666666666666,0.33725490196078434,0.7803921568627451,1;rgb;ccw:0.0976563;69,89,203,255,rgb:0.27058823529411763,0.34901960784313724,0.79607843137254897,1;rgb;ccw:0.101563;69,92,207,255,rgb:0.27058823529411763,0.36078431372549019,0.81176470588235294,1;rgb;ccw:0.105469;69,94,211,255,rgb:0.27058823529411763,0.36862745098039218,0.82745098039215681,1;rgb;ccw:0.109375;70,97,214,255,rgb:0.27450980392156865,0.38039215686274508,0.83921568627450982,1;rgb;ccw:0.113281;70,100,218,255,rgb:0.27450980392156865,0.39215686274509803,0.85490196078431369,1;rgb;ccw:0.117188;70,102,221,255,rgb:0.27450980392156865,0.40000000000000002,0.8666666666666667,1;rgb;ccw:0.121094;70,105,224,255,rgb:0.27450980392156865,0.41176470588235292,0.8784313725490196,1;rgb;ccw:0.125;70,107,227,255,rgb:0.27450980392156865,0.41960784313725491,0.8901960784313725,1;rgb;ccw:0.128906;71,110,230,255,rgb:0.27843137254901962,0.43137254901960786,0.90196078431372551,1;rgb;ccw:0.132813;71,113,233,255,rgb:0.27843137254901962,0.44313725490196076,0.9137254901960784,1;rgb;ccw:0.136719;71,115,235,255,rgb:0.27843137254901962,0.45098039215686275,0.92156862745098034,1;rgb;ccw:0.140625;71,118,238,255,rgb:0.27843137254901962,0.46274509803921571,0.93333333333333335,1;rgb;ccw:0.144531;71,120,240,255,rgb:0.27843137254901962,0.47058823529411764,0.94117647058823528,1;rgb;ccw:0.148438;71,123,242,255,rgb:0.27843137254901962,0.4823529411764706,0.94901960784313721,1;rgb;ccw:0.152344;70,125,244,255,rgb:0.27450980392156865,0.49019607843137253,0.95686274509803926,1;rgb;ccw:0.15625;70,128,246,255,rgb:0.27450980392156865,0.50196078431372548,0.96470588235294119,1;rgb;ccw:0.160156;70,130,248,255,rgb:0.27450980392156865,0.50980392156862742,0.97254901960784312,1;rgb;ccw:0.164063;70,133,250,255,rgb:0.27450980392156865,0.52156862745098043,0.98039215686274506,1;rgb;ccw:0.167969;70,135,251,255,rgb:0.27450980392156865,0.52941176470588236,0.98431372549019602,1;rgb;ccw:0.171875;69,138,252,255,rgb:0.27058823529411763,0.54117647058823526,0.9882352941176471,1;rgb;ccw:0.175781;69,140,253,255,rgb:0.27058823529411763,0.5490196078431373,0.99215686274509807,1;rgb;ccw:0.179688;68,143,254,255,rgb:0.26666666666666666,0.5607843137254902,0.99607843137254903,1;rgb;ccw:0.183594;67,145,254,255,rgb:0.2627450980392157,0.56862745098039214,0.99607843137254903,1;rgb;ccw:0.1875;66,148,255,255,rgb:0.25882352941176473,0.58039215686274515,1,1;rgb;ccw:0.191406;65,150,255,255,rgb:0.25490196078431371,0.58823529411764708,1,1;rgb;ccw:0.195313;64,153,255,255,rgb:0.25098039215686274,0.59999999999999998,1,1;rgb;ccw:0.199219;62,155,254,255,rgb:0.24313725490196078,0.60784313725490191,0.99607843137254903,1;rgb;ccw:0.203125;61,158,254,255,rgb:0.23921568627450981,0.61960784313725492,0.99607843137254903,1;rgb;ccw:0.207031;59,160,253,255,rgb:0.23137254901960785,0.62745098039215685,0.99215686274509807,1;rgb;ccw:0.210938;58,163,252,255,rgb:0.22745098039215686,0.63921568627450975,0.9882352941176471,1;rgb;ccw:0.214844;56,165,251,255,rgb:0.2196078431372549,0.6470588235294118,0.98431372549019602,1;rgb;ccw:0.21875;55,168,250,255,rgb:0.21568627450980393,0.6588235294117647,0.98039215686274506,1;rgb;ccw:0.222656;53,171,248,255,rgb:0.20784313725490197,0.6705882352941176,0.97254901960784312,1;rgb;ccw:0.226563;51,173,247,255,rgb:0.20000000000000001,0.67843137254901964,0.96862745098039216,1;rgb;ccw:0.230469;49,175,245,255,rgb:0.19215686274509805,0.68627450980392157,0.96078431372549022,1;rgb;ccw:0.234375;47,178,244,255,rgb:0.18431372549019609,0.69803921568627447,0.95686274509803926,1;rgb;ccw:0.238281;46,180,242,255,rgb:0.1803921568627451,0.70588235294117652,0.94901960784313721,1;rgb;ccw:0.242188;44,183,240,255,rgb:0.17254901960784313,0.71764705882352942,0.94117647058823528,1;rgb;ccw:0.246094;42,185,238,255,rgb:0.16470588235294117,0.72549019607843135,0.93333333333333335,1;rgb;ccw:0.25;40,188,235,255,rgb:0.15686274509803921,0.73725490196078436,0.92156862745098034,1;rgb;ccw:0.253906;39,190,233,255,rgb:0.15294117647058825,0.74509803921568629,0.9137254901960784,1;rgb;ccw:0.257813;37,192,231,255,rgb:0.14509803921568629,0.75294117647058822,0.90588235294117647,1;rgb;ccw:0.261719;35,195,228,255,rgb:0.13725490196078433,0.76470588235294112,0.89411764705882357,1;rgb;ccw:0.265625;34,197,226,255,rgb:0.13333333333333333,0.77254901960784317,0.88627450980392153,1;rgb;ccw:0.269531;32,199,223,255,rgb:0.12549019607843137,0.7803921568627451,0.87450980392156863,1;rgb;ccw:0.273438;31,201,221,255,rgb:0.12156862745098039,0.78823529411764703,0.8666666666666667,1;rgb;ccw:0.277344;30,203,218,255,rgb:0.11764705882352941,0.79607843137254897,0.85490196078431369,1;rgb;ccw:0.28125;28,205,216,255,rgb:0.10980392156862745,0.80392156862745101,0.84705882352941175,1;rgb;ccw:0.285156;27,208,213,255,rgb:0.10588235294117647,0.81568627450980391,0.83529411764705885,1;rgb;ccw:0.289063;26,210,210,255,rgb:0.10196078431372549,0.82352941176470584,0.82352941176470584,1;rgb;ccw:0.292969;26,212,208,255,rgb:0.10196078431372549,0.83137254901960789,0.81568627450980391,1;rgb;ccw:0.296875;25,213,205,255,rgb:0.09803921568627451,0.83529411764705885,0.80392156862745101,1;rgb;ccw:0.300781;24,215,202,255,rgb:0.09411764705882353,0.84313725490196079,0.792156862745098,1;rgb;ccw:0.304688;24,217,200,255,rgb:0.09411764705882353,0.85098039215686272,0.78431372549019607,1;rgb;ccw:0.308594;24,219,197,255,rgb:0.09411764705882353,0.85882352941176465,0.77254901960784317,1;rgb;ccw:0.3125;24,221,194,255,rgb:0.09411764705882353,0.8666666666666667,0.76078431372549016,1;rgb;ccw:0.316406;24,222,192,255,rgb:0.09411764705882353,0.87058823529411766,0.75294117647058822,1;rgb;ccw:0.320313;24,224,189,255,rgb:0.09411764705882353,0.8784313725490196,0.74117647058823533,1;rgb;ccw:0.324219;25,226,187,255,rgb:0.09803921568627451,0.88627450980392153,0.73333333333333328,1;rgb;ccw:0.328125;25,227,185,255,rgb:0.09803921568627451,0.8901960784313725,0.72549019607843135,1;rgb;ccw:0.332031;26,228,182,255,rgb:0.10196078431372549,0.89411764705882357,0.71372549019607845,1;rgb;ccw:0.335938;28,230,180,255,rgb:0.10980392156862745,0.90196078431372551,0.70588235294117652,1;rgb;ccw:0.339844;29,231,178,255,rgb:0.11372549019607843,0.90588235294117647,0.69803921568627447,1;rgb;ccw:0.34375;31,233,175,255,rgb:0.12156862745098039,0.9137254901960784,0.68627450980392157,1;rgb;ccw:0.347656;32,234,172,255,rgb:0.12549019607843137,0.91764705882352937,0.67450980392156867,1;rgb;ccw:0.351563;34,235,170,255,rgb:0.13333333333333333,0.92156862745098034,0.66666666666666663,1;rgb;ccw:0.355469;37,236,167,255,rgb:0.14509803921568629,0.92549019607843142,0.65490196078431373,1;rgb;ccw:0.359375;39,238,164,255,rgb:0.15294117647058825,0.93333333333333335,0.64313725490196083,1;rgb;ccw:0.363281;42,239,161,255,rgb:0.16470588235294117,0.93725490196078431,0.63137254901960782,1;rgb;ccw:0.367188;44,240,158,255,rgb:0.17254901960784313,0.94117647058823528,0.61960784313725492,1;rgb;ccw:0.371094;47,241,155,255,rgb:0.18431372549019609,0.94509803921568625,0.60784313725490191,1;rgb;ccw:0.375;50,242,152,255,rgb:0.19607843137254902,0.94901960784313721,0.59607843137254901,1;rgb;ccw:0.378906;53,243,148,255,rgb:0.20784313725490197,0.95294117647058818,0.58039215686274515,1;rgb;ccw:0.382813;56,244,145,255,rgb:0.2196078431372549,0.95686274509803926,0.56862745098039214,1;rgb;ccw:0.386719;60,245,142,255,rgb:0.23529411764705882,0.96078431372549022,0.55686274509803924,1;rgb;ccw:0.390625;63,246,138,255,rgb:0.24705882352941178,0.96470588235294119,0.54117647058823526,1;rgb;ccw:0.394531;67,247,135,255,rgb:0.2627450980392157,0.96862745098039216,0.52941176470588236,1;rgb;ccw:0.398438;70,248,132,255,rgb:0.27450980392156865,0.97254901960784312,0.51764705882352946,1;rgb;ccw:0.402344;74,248,128,255,rgb:0.29019607843137257,0.97254901960784312,0.50196078431372548,1;rgb;ccw:0.40625;78,249,125,255,rgb:0.30588235294117649,0.97647058823529409,0.49019607843137253,1;rgb;ccw:0.410156;82,250,122,255,rgb:0.32156862745098042,0.98039215686274506,0.47843137254901963,1;rgb;ccw:0.414063;85,250,118,255,rgb:0.33333333333333331,0.98039215686274506,0.46274509803921571,1;rgb;ccw:0.417969;89,251,115,255,rgb:0.34901960784313724,0.98431372549019602,0.45098039215686275,1;rgb;ccw:0.421875;93,252,111,255,rgb:0.36470588235294116,0.9882352941176471,0.43529411764705883,1;rgb;ccw:0.425781;97,252,108,255,rgb:0.38039215686274508,0.9882352941176471,0.42352941176470588,1;rgb;ccw:0.429688;101,253,105,255,rgb:0.396078431372549,0.99215686274509807,0.41176470588235292,1;rgb;ccw:0.433594;105,253,102,255,rgb:0.41176470588235292,0.99215686274509807,0.40000000000000002,1;rgb;ccw:0.4375;109,254,98,255,rgb:0.42745098039215684,0.99607843137254903,0.3843137254901961,1;rgb;ccw:0.441406;113,254,95,255,rgb:0.44313725490196076,0.99607843137254903,0.37254901960784315,1;rgb;ccw:0.445313;117,254,92,255,rgb:0.45882352941176469,0.99607843137254903,0.36078431372549019,1;rgb;ccw:0.449219;121,254,89,255,rgb:0.47450980392156861,0.99607843137254903,0.34901960784313724,1;rgb;ccw:0.453125;125,255,86,255,rgb:0.49019607843137253,1,0.33725490196078434,1;rgb;ccw:0.457031;128,255,83,255,rgb:0.50196078431372548,1,0.32549019607843138,1;rgb;ccw:0.460938;132,255,81,255,rgb:0.51764705882352946,1,0.31764705882352939,1;rgb;ccw:0.464844;136,255,78,255,rgb:0.53333333333333333,1,0.30588235294117649,1;rgb;ccw:0.46875;139,255,75,255,rgb:0.54509803921568623,1,0.29411764705882354,1;rgb;ccw:0.472656;143,255,73,255,rgb:0.5607843137254902,1,0.28627450980392155,1;rgb;ccw:0.476563;146,255,71,255,rgb:0.5725490196078431,1,0.27843137254901962,1;rgb;ccw:0.480469;150,254,68,255,rgb:0.58823529411764708,0.99607843137254903,0.26666666666666666,1;rgb;ccw:0.484375;153,254,66,255,rgb:0.59999999999999998,0.99607843137254903,0.25882352941176473,1;rgb;ccw:0.488281;156,254,64,255,rgb:0.61176470588235299,0.99607843137254903,0.25098039215686274,1;rgb;ccw:0.492188;159,253,63,255,rgb:0.62352941176470589,0.99215686274509807,0.24705882352941178,1;rgb;ccw:0.496094;161,253,61,255,rgb:0.63137254901960782,0.99215686274509807,0.23921568627450981,1;rgb;ccw:0.5;164,252,60,255,rgb:0.64313725490196083,0.9882352941176471,0.23529411764705882,1;rgb;ccw:0.503906;167,252,58,255,rgb:0.65490196078431373,0.9882352941176471,0.22745098039215686,1;rgb;ccw:0.507813;169,251,57,255,rgb:0.66274509803921566,0.98431372549019602,0.22352941176470589,1;rgb;ccw:0.511719;172,251,56,255,rgb:0.67450980392156867,0.98431372549019602,0.2196078431372549,1;rgb;ccw:0.515625;175,250,55,255,rgb:0.68627450980392157,0.98039215686274506,0.21568627450980393,1;rgb;ccw:0.519531;177,249,54,255,rgb:0.69411764705882351,0.97647058823529409,0.21176470588235294,1;rgb;ccw:0.523438;180,248,54,255,rgb:0.70588235294117652,0.97254901960784312,0.21176470588235294,1;rgb;ccw:0.527344;183,247,53,255,rgb:0.71764705882352942,0.96862745098039216,0.20784313725490197,1;rgb;ccw:0.53125;185,246,53,255,rgb:0.72549019607843135,0.96470588235294119,0.20784313725490197,1;rgb;ccw:0.535156;188,245,52,255,rgb:0.73725490196078436,0.96078431372549022,0.20392156862745098,1;rgb;ccw:0.539063;190,244,52,255,rgb:0.74509803921568629,0.95686274509803926,0.20392156862745098,1;rgb;ccw:0.542969;193,243,52,255,rgb:0.75686274509803919,0.95294117647058818,0.20392156862745098,1;rgb;ccw:0.546875;195,241,52,255,rgb:0.76470588235294112,0.94509803921568625,0.20392156862745098,1;rgb;ccw:0.550781;198,240,52,255,rgb:0.77647058823529413,0.94117647058823528,0.20392156862745098,1;rgb;ccw:0.554688;200,239,52,255,rgb:0.78431372549019607,0.93725490196078431,0.20392156862745098,1;rgb;ccw:0.558594;203,237,52,255,rgb:0.79607843137254897,0.92941176470588238,0.20392156862745098,1;rgb;ccw:0.5625;205,236,52,255,rgb:0.80392156862745101,0.92549019607843142,0.20392156862745098,1;rgb;ccw:0.566406;208,234,52,255,rgb:0.81568627450980391,0.91764705882352937,0.20392156862745098,1;rgb;ccw:0.570313;210,233,53,255,rgb:0.82352941176470584,0.9137254901960784,0.20784313725490197,1;rgb;ccw:0.574219;212,231,53,255,rgb:0.83137254901960789,0.90588235294117647,0.20784313725490197,1;rgb;ccw:0.578125;215,229,53,255,rgb:0.84313725490196079,0.89803921568627454,0.20784313725490197,1;rgb;ccw:0.582031;217,228,54,255,rgb:0.85098039215686272,0.89411764705882357,0.21176470588235294,1;rgb;ccw:0.585938;219,226,54,255,rgb:0.85882352941176465,0.88627450980392153,0.21176470588235294,1;rgb;ccw:0.589844;221,224,55,255,rgb:0.8666666666666667,0.8784313725490196,0.21568627450980393,1;rgb;ccw:0.59375;223,223,55,255,rgb:0.87450980392156863,0.87450980392156863,0.21568627450980393,1;rgb;ccw:0.597656;225,221,55,255,rgb:0.88235294117647056,0.8666666666666667,0.21568627450980393,1;rgb;ccw:0.601563;227,219,56,255,rgb:0.8901960784313725,0.85882352941176465,0.2196078431372549,1;rgb;ccw:0.605469;229,217,56,255,rgb:0.89803921568627454,0.85098039215686272,0.2196078431372549,1;rgb;ccw:0.609375;231,215,57,255,rgb:0.90588235294117647,0.84313725490196079,0.22352941176470589,1;rgb;ccw:0.613281;233,213,57,255,rgb:0.9137254901960784,0.83529411764705885,0.22352941176470589,1;rgb;ccw:0.617188;235,211,57,255,rgb:0.92156862745098034,0.82745098039215681,0.22352941176470589,1;rgb;ccw:0.621094;236,209,58,255,rgb:0.92549019607843142,0.81960784313725488,0.22745098039215686,1;rgb;ccw:0.625;238,207,58,255,rgb:0.93333333333333335,0.81176470588235294,0.22745098039215686,1;rgb;ccw:0.628906;239,205,58,255,rgb:0.93725490196078431,0.80392156862745101,0.22745098039215686,1;rgb;ccw:0.632813;241,203,58,255,rgb:0.94509803921568625,0.79607843137254897,0.22745098039215686,1;rgb;ccw:0.636719;242,201,58,255,rgb:0.94901960784313721,0.78823529411764703,0.22745098039215686,1;rgb;ccw:0.640625;244,199,58,255,rgb:0.95686274509803926,0.7803921568627451,0.22745098039215686,1;rgb;ccw:0.644531;245,197,58,255,rgb:0.96078431372549022,0.77254901960784317,0.22745098039215686,1;rgb;ccw:0.648438;246,195,58,255,rgb:0.96470588235294119,0.76470588235294112,0.22745098039215686,1;rgb;ccw:0.652344;247,193,58,255,rgb:0.96862745098039216,0.75686274509803919,0.22745098039215686,1;rgb;ccw:0.65625;248,190,57,255,rgb:0.97254901960784312,0.74509803921568629,0.22352941176470589,1;rgb;ccw:0.660156;249,188,57,255,rgb:0.97647058823529409,0.73725490196078436,0.22352941176470589,1;rgb;ccw:0.664063;250,186,57,255,rgb:0.98039215686274506,0.72941176470588232,0.22352941176470589,1;rgb;ccw:0.667969;251,184,56,255,rgb:0.98431372549019602,0.72156862745098038,0.2196078431372549,1;rgb;ccw:0.671875;251,182,55,255,rgb:0.98431372549019602,0.71372549019607845,0.21568627450980393,1;rgb;ccw:0.675781;252,179,54,255,rgb:0.9882352941176471,0.70196078431372544,0.21176470588235294,1;rgb;ccw:0.679688;252,177,54,255,rgb:0.9882352941176471,0.69411764705882351,0.21176470588235294,1;rgb;ccw:0.683594;253,174,53,255,rgb:0.99215686274509807,0.68235294117647061,0.20784313725490197,1;rgb;ccw:0.6875;253,172,52,255,rgb:0.99215686274509807,0.67450980392156867,0.20392156862745098,1;rgb;ccw:0.691406;254,169,51,255,rgb:0.99607843137254903,0.66274509803921566,0.20000000000000001,1;rgb;ccw:0.695313;254,167,50,255,rgb:0.99607843137254903,0.65490196078431373,0.19607843137254902,1;rgb;ccw:0.699219;254,164,49,255,rgb:0.99607843137254903,0.64313725490196083,0.19215686274509805,1;rgb;ccw:0.703125;254,161,48,255,rgb:0.99607843137254903,0.63137254901960782,0.18823529411764706,1;rgb;ccw:0.707031;254,158,47,255,rgb:0.99607843137254903,0.61960784313725492,0.18431372549019609,1;rgb;ccw:0.710938;254,155,45,255,rgb:0.99607843137254903,0.60784313725490191,0.17647058823529413,1;rgb;ccw:0.714844;254,153,44,255,rgb:0.99607843137254903,0.59999999999999998,0.17254901960784313,1;rgb;ccw:0.71875;254,150,43,255,rgb:0.99607843137254903,0.58823529411764708,0.16862745098039217,1;rgb;ccw:0.722656;254,147,42,255,rgb:0.99607843137254903,0.57647058823529407,0.16470588235294117,1;rgb;ccw:0.726563;254,144,41,255,rgb:0.99607843137254903,0.56470588235294117,0.16078431372549021,1;rgb;ccw:0.730469;253,141,39,255,rgb:0.99215686274509807,0.55294117647058827,0.15294117647058825,1;rgb;ccw:0.734375;253,138,38,255,rgb:0.99215686274509807,0.54117647058823526,0.14901960784313725,1;rgb;ccw:0.738281;252,135,37,255,rgb:0.9882352941176471,0.52941176470588236,0.14509803921568629,1;rgb;ccw:0.742188;252,132,35,255,rgb:0.9882352941176471,0.51764705882352946,0.13725490196078433,1;rgb;ccw:0.746094;251,129,34,255,rgb:0.98431372549019602,0.50588235294117645,0.13333333333333333,1;rgb;ccw:0.75;251,126,33,255,rgb:0.98431372549019602,0.49411764705882355,0.12941176470588237,1;rgb;ccw:0.753906;250,123,31,255,rgb:0.98039215686274506,0.4823529411764706,0.12156862745098039,1;rgb;ccw:0.757813;249,120,30,255,rgb:0.97647058823529409,0.47058823529411764,0.11764705882352941,1;rgb;ccw:0.761719;249,117,29,255,rgb:0.97647058823529409,0.45882352941176469,0.11372549019607843,1;rgb;ccw:0.765625;248,114,28,255,rgb:0.97254901960784312,0.44705882352941179,0.10980392156862745,1;rgb;ccw:0.769531;247,111,26,255,rgb:0.96862745098039216,0.43529411764705883,0.10196078431372549,1;rgb;ccw:0.773438;246,108,25,255,rgb:0.96470588235294119,0.42352941176470588,0.09803921568627451,1;rgb;ccw:0.777344;245,105,24,255,rgb:0.96078431372549022,0.41176470588235292,0.09411764705882353,1;rgb;ccw:0.78125;244,102,23,255,rgb:0.95686274509803926,0.40000000000000002,0.09019607843137255,1;rgb;ccw:0.785156;243,99,21,255,rgb:0.95294117647058818,0.38823529411764707,0.08235294117647059,1;rgb;ccw:0.789063;242,96,20,255,rgb:0.94901960784313721,0.37647058823529411,0.07843137254901961,1;rgb;ccw:0.792969;241,93,19,255,rgb:0.94509803921568625,0.36470588235294116,0.07450980392156863,1;rgb;ccw:0.796875;240,91,18,255,rgb:0.94117647058823528,0.35686274509803922,0.07058823529411765,1;rgb;ccw:0.800781;239,88,17,255,rgb:0.93725490196078431,0.34509803921568627,0.06666666666666667,1;rgb;ccw:0.804688;237,85,16,255,rgb:0.92941176470588238,0.33333333333333331,0.06274509803921569,1;rgb;ccw:0.808594;236,83,15,255,rgb:0.92549019607843142,0.32549019607843138,0.05882352941176471,1;rgb;ccw:0.8125;235,80,14,255,rgb:0.92156862745098034,0.31372549019607843,0.05490196078431372,1;rgb;ccw:0.816406;234,78,13,255,rgb:0.91764705882352937,0.30588235294117649,0.05098039215686274,1;rgb;ccw:0.820313;232,75,12,255,rgb:0.90980392156862744,0.29411764705882354,0.04705882352941176,1;rgb;ccw:0.824219;231,73,12,255,rgb:0.90588235294117647,0.28627450980392155,0.04705882352941176,1;rgb;ccw:0.828125;229,71,11,255,rgb:0.89803921568627454,0.27843137254901962,0.04313725490196078,1;rgb;ccw:0.832031;228,69,10,255,rgb:0.89411764705882357,0.27058823529411763,0.0392156862745098,1;rgb;ccw:0.835938;226,67,10,255,rgb:0.88627450980392153,0.2627450980392157,0.0392156862745098,1;rgb;ccw:0.839844;225,65,9,255,rgb:0.88235294117647056,0.25490196078431371,0.03529411764705882,1;rgb;ccw:0.84375;223,63,8,255,rgb:0.87450980392156863,0.24705882352941178,0.03137254901960784,1;rgb;ccw:0.847656;221,61,8,255,rgb:0.8666666666666667,0.23921568627450981,0.03137254901960784,1;rgb;ccw:0.851563;220,59,7,255,rgb:0.86274509803921573,0.23137254901960785,0.02745098039215686,1;rgb;ccw:0.855469;218,57,7,255,rgb:0.85490196078431369,0.22352941176470589,0.02745098039215686,1;rgb;ccw:0.859375;216,55,6,255,rgb:0.84705882352941175,0.21568627450980393,0.02352941176470588,1;rgb;ccw:0.863281;214,53,6,255,rgb:0.83921568627450982,0.20784313725490197,0.02352941176470588,1;rgb;ccw:0.867188;212,51,5,255,rgb:0.83137254901960789,0.20000000000000001,0.0196078431372549,1;rgb;ccw:0.871094;210,49,5,255,rgb:0.82352941176470584,0.19215686274509805,0.0196078431372549,1;rgb;ccw:0.875;208,47,5,255,rgb:0.81568627450980391,0.18431372549019609,0.0196078431372549,1;rgb;ccw:0.878906;206,45,4,255,rgb:0.80784313725490198,0.17647058823529413,0.01568627450980392,1;rgb;ccw:0.882813;204,43,4,255,rgb:0.80000000000000004,0.16862745098039217,0.01568627450980392,1;rgb;ccw:0.886719;202,42,4,255,rgb:0.792156862745098,0.16470588235294117,0.01568627450980392,1;rgb;ccw:0.890625;200,40,3,255,rgb:0.78431372549019607,0.15686274509803921,0.01176470588235294,1;rgb;ccw:0.894531;197,38,3,255,rgb:0.77254901960784317,0.14901960784313725,0.01176470588235294,1;rgb;ccw:0.898438;195,37,3,255,rgb:0.76470588235294112,0.14509803921568629,0.01176470588235294,1;rgb;ccw:0.902344;193,35,2,255,rgb:0.75686274509803919,0.13725490196078433,0.00784313725490196,1;rgb;ccw:0.90625;190,33,2,255,rgb:0.74509803921568629,0.12941176470588237,0.00784313725490196,1;rgb;ccw:0.910156;188,32,2,255,rgb:0.73725490196078436,0.12549019607843137,0.00784313725490196,1;rgb;ccw:0.914063;185,30,2,255,rgb:0.72549019607843135,0.11764705882352941,0.00784313725490196,1;rgb;ccw:0.917969;183,29,2,255,rgb:0.71764705882352942,0.11372549019607843,0.00784313725490196,1;rgb;ccw:0.921875;180,27,1,255,rgb:0.70588235294117652,0.10588235294117647,0.00392156862745098,1;rgb;ccw:0.925781;178,26,1,255,rgb:0.69803921568627447,0.10196078431372549,0.00392156862745098,1;rgb;ccw:0.929688;175,24,1,255,rgb:0.68627450980392157,0.09411764705882353,0.00392156862745098,1;rgb;ccw:0.933594;172,23,1,255,rgb:0.67450980392156867,0.09019607843137255,0.00392156862745098,1;rgb;ccw:0.9375;169,22,1,255,rgb:0.66274509803921566,0.08627450980392157,0.00392156862745098,1;rgb;ccw:0.941406;167,20,1,255,rgb:0.65490196078431373,0.07843137254901961,0.00392156862745098,1;rgb;ccw:0.945313;164,19,1,255,rgb:0.64313725490196083,0.07450980392156863,0.00392156862745098,1;rgb;ccw:0.949219;161,18,1,255,rgb:0.63137254901960782,0.07058823529411765,0.00392156862745098,1;rgb;ccw:0.953125;158,16,1,255,rgb:0.61960784313725492,0.06274509803921569,0.00392156862745098,1;rgb;ccw:0.957031;155,15,1,255,rgb:0.60784313725490191,0.05882352941176471,0.00392156862745098,1;rgb;ccw:0.960938;152,14,1,255,rgb:0.59607843137254901,0.05490196078431372,0.00392156862745098,1;rgb;ccw:0.964844;149,13,1,255,rgb:0.58431372549019611,0.05098039215686274,0.00392156862745098,1;rgb;ccw:0.96875;146,11,1,255,rgb:0.5725490196078431,0.04313725490196078,0.00392156862745098,1;rgb;ccw:0.972656;142,10,1,255,rgb:0.55686274509803924,0.0392156862745098,0.00392156862745098,1;rgb;ccw:0.976563;139,9,2,255,rgb:0.54509803921568623,0.03529411764705882,0.00784313725490196,1;rgb;ccw:0.980469;136,8,2,255,rgb:0.53333333333333333,0.03137254901960784,0.00784313725490196,1;rgb;ccw:0.984375;133,7,2,255,rgb:0.52156862745098043,0.02745098039215686,0.00784313725490196,1;rgb;ccw:0.988281;129,6,2,255,rgb:0.50588235294117645,0.02352941176470588,0.00784313725490196,1;rgb;ccw" type="QString" name="stops"/>
      </Option>
    </colorramp>
    <classificationMethod id="Fixed">
      <symmetricMode enabled="0" symmetrypoint="0" astride="0"/>
      <labelFormat format="%1 - %2" labelprecision="2" trimtrailingzeroes="1"/>
      <parameters>
        <Option type="Map">
          <Option value="0.25" type="double" name="INTERVAL"/>
        </Option>
      </parameters>
      <extraInformation/>
    </classificationMethod>
    <rotation/>
    <sizescale/>
    <data-defined-properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </data-defined-properties>
  </renderer-v2>
  <selection mode="Default">
    <selectionColor invalid="1"/>
    <selectionSymbol>
      <symbol clip_to_extent="1" type="marker" frame_rate="10" alpha="1" force_rhr="0" name="" is_animated="0">
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0" id="{817bff15-427a-4f93-a665-775072a18817}">
          <Option type="Map">
            <Option value="0" type="QString" name="angle"/>
            <Option value="square" type="QString" name="cap_style"/>
            <Option value="255,0,0,255,rgb:1,0,0,1" type="QString" name="color"/>
            <Option value="1" type="QString" name="horizontal_anchor_point"/>
            <Option value="bevel" type="QString" name="joinstyle"/>
            <Option value="circle" type="QString" name="name"/>
            <Option value="0,0" type="QString" name="offset"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="offset_map_unit_scale"/>
            <Option value="MM" type="QString" name="offset_unit"/>
            <Option value="35,35,35,255,rgb:0.13725490196078433,0.13725490196078433,0.13725490196078433,1" type="QString" name="outline_color"/>
            <Option value="solid" type="QString" name="outline_style"/>
            <Option value="0" type="QString" name="outline_width"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="outline_width_map_unit_scale"/>
            <Option value="MM" type="QString" name="outline_width_unit"/>
            <Option value="diameter" type="QString" name="scale_method"/>
            <Option value="2" type="QString" name="size"/>
            <Option value="3x:0,0,0,0,0,0" type="QString" name="size_map_unit_scale"/>
            <Option value="MM" type="QString" name="size_unit"/>
            <Option value="1" type="QString" name="vertical_anchor_point"/>
          </Option>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </selectionSymbol>
  </selection>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <legend type="default-vector" showLabelLegend="0"/>
  <fieldConfiguration>
    <field configurationFlags="NoFlag" name="pk"/>
    <field configurationFlags="NoFlag" name="v"/>
    <field configurationFlags="NoFlag" name="angle"/>
    <field configurationFlags="NoFlag" name="tanf"/>
    <field configurationFlags="NoFlag" name="tend"/>
  </fieldConfiguration>
  <aliases>
    <alias field="pk" index="0" name=""/>
    <alias field="v" index="1" name=""/>
    <alias field="angle" index="2" name=""/>
    <alias field="tanf" index="3" name=""/>
    <alias field="tend" index="4" name=""/>
  </aliases>
  <splitPolicies>
    <policy field="pk" policy="Duplicate"/>
    <policy field="v" policy="Duplicate"/>
    <policy field="angle" policy="Duplicate"/>
    <policy field="tanf" policy="Duplicate"/>
    <policy field="tend" policy="Duplicate"/>
  </splitPolicies>
  <duplicatePolicies>
    <policy field="pk" policy="Duplicate"/>
    <policy field="v" policy="Duplicate"/>
    <policy field="angle" policy="Duplicate"/>
    <policy field="tanf" policy="Duplicate"/>
    <policy field="tend" policy="Duplicate"/>
  </duplicatePolicies>
  <defaults>
    <default applyOnUpdate="0" field="pk" expression=""/>
    <default applyOnUpdate="0" field="v" expression=""/>
    <default applyOnUpdate="0" field="angle" expression=""/>
    <default applyOnUpdate="0" field="tanf" expression=""/>
    <default applyOnUpdate="0" field="tend" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" exp_strength="0" field="pk" notnull_strength="1" constraints="3"/>
    <constraint unique_strength="0" exp_strength="0" field="v" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="angle" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="tanf" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="tend" notnull_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="pk" desc=""/>
    <constraint exp="" field="v" desc=""/>
    <constraint exp="" field="angle" desc=""/>
    <constraint exp="" field="tanf" desc=""/>
    <constraint exp="" field="tend" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns>
      <column type="field" width="-1" name="pk" hidden="0"/>
      <column type="field" width="144" name="v" hidden="0"/>
      <column type="field" width="-1" name="angle" hidden="0"/>
      <column type="field" width="-1" name="tanf" hidden="0"/>
      <column type="field" width="-1" name="tend" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <previewExpression>"tanf"</previewExpression>
  <mapTip enabled="1"></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
