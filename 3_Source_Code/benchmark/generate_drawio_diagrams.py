"""
Generate editable Draw.io XML diagrams for Figures 1, 2, and 8.
Ensures compliance with Guideline: "Re-draw diagrams using draw.io for clarity and originality".
"""

import os

diagrams_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "2_Diagrams"))

# 1. Fig 01 Architecture
fig01_xml = """<mxfile host="app.diagrams.net">
  <diagram id="arch-diagram" name="AI-Driven Privacy Compliance Architecture">
    <mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="850">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- IoT Sources -->
        <mxCell id="sources" value="IoT SOURCES&#xa;wearables • sensors • cameras • meters • industrial devices" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="250" y="40" width="500" height="50" as="geometry" />
        </mxCell>

        <!-- Secure Gateway -->
        <mxCell id="gateway" value="SECURE GATEWAY&#xa;identity • schema validation • source and purpose metadata" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="250" y="130" width="500" height="50" as="geometry" />
        </mxCell>

        <!-- Edge Privacy Controls -->
        <mxCell id="edge" value="EDGE PRIVACY CONTROLS&#xa;data labels • minimisation • local policy • retention check" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="250" y="220" width="500" height="50" as="geometry" />
        </mxCell>

        <!-- AI Risk Engine -->
        <mxCell id="risk" value="AI RISK ENGINE&#xa;anomaly score • reasons • uncertainty" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="200" y="320" width="280" height="50" as="geometry" />
        </mxCell>

        <!-- Policy Engine -->
        <mxCell id="policy" value="POLICY ENGINE&#xa;mandatory rules • purpose • receiver • expiry" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="520" y="320" width="280" height="50" as="geometry" />
        </mxCell>

        <!-- Decision + Governance -->
        <mxCell id="decision" value="DECISION + GOVERNANCE&#xa;allow • minimise • transform • block • human review • audit record" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="250" y="420" width="500" height="50" as="geometry" />
        </mxCell>

        <!-- Connectors -->
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="sources" target="gateway">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="gateway" target="edge">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="edge" target="risk">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="edge" target="policy">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="risk" target="decision">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="policy" target="decision">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

# 2. Fig 02 Pipeline
fig02_xml = """<mxfile host="app.diagrams.net">
  <diagram id="pipeline-diagram" name="End-to-End Privacy Compliance Pipeline">
    <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="s1" value="1. Capture event and needed metadata" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="40" width="350" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s2" value="2. Verify device and required fields" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="110" width="350" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s3" value="3. Label data and purpose" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="180" width="350" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s4" value="4. Apply mandatory privacy rules" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="250" width="350" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s5" value="5. Calculate risk score and reasons" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="320" width="350" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s6" value="6. Choose action from policy" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="390" width="350" height="40" as="geometry" />
        </mxCell>
        <mxCell id="s7" value="7. Save audit evidence and show result" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="250" y="460" width="350" height="40" as="geometry" />
        </mxCell>

        <!-- Arrows -->
        <mxCell id="a1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s1" target="s2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="a2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s2" target="s3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="a3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s3" target="s4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="a4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s4" target="s5"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="a5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s5" target="s6"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="a6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s6" target="s7"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

# 3. Fig 08 Compliance Decision
fig08_xml = """<mxfile host="app.diagrams.net">
  <diagram id="decision-diagram" name="Example Compliance Decision">
    <mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="600">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <mxCell id="inp" value="INPUT&#xa;Wearable health-data request" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="280" y="40" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="pol_check" value="POLICY CHECK&#xa;Receiver not approved&#xa;Mandatory deny rule" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="180" y="140" width="200" height="60" as="geometry" />
        </mxCell>
        <mxCell id="ai_risk" value="AI RISK&#xa;86 / 100&#xa;Illustrative only" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="460" y="140" width="200" height="60" as="geometry" />
        </mxCell>
        <mxCell id="block" value="BLOCK&#xa;Stop transfer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="180" y="250" width="200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="alert" value="ALERT / REVIEW&#xa;Notify owner" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="460" y="250" width="200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="audit" value="AUDIT RECORD SAVED&#xa;Reason • policy version • timestamp" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="230" y="350" width="380" height="50" as="geometry" />
        </mxCell>

        <!-- Edges -->
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="inp" target="pol_check"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="inp" target="ai_risk"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="pol_check" target="block"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="ai_risk" target="alert"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="block" target="audit"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="alert" target="audit"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

with open(os.path.join(diagrams_dir, "Fig 01 - AI-Driven Privacy Compliance Architecture.drawio"), "w", encoding="utf-8") as f:
    f.write(fig01_xml)

with open(os.path.join(diagrams_dir, "Fig 02 - End-to-End Privacy Compliance Pipeline.drawio"), "w", encoding="utf-8") as f:
    f.write(fig02_xml)

with open(os.path.join(diagrams_dir, "Fig 08 - Example System Output - Compliance Decision.drawio"), "w", encoding="utf-8") as f:
    f.write(fig08_xml)

print("[+] Created editable draw.io XML files in 2_Diagrams!")
