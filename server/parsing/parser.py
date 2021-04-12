import xml.etree.ElementTree as ET
import base64

NAMESPACE = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"


# Converts a Base 64 encoded BPMN DI string to a text
def convert_bpmn_to_text(bpmn_di_b64enc: str):
    bpmn_di = b64dec(bpmn_di_b64enc)

    tree = ET.ElementTree(ET.fromstring(bpmn_di))
    root = tree.getroot()
    process = root.find(f"{NAMESPACE}process")
    bpmn_elements, start_event_id = parse_bpmn_di(process)
    add_missing_outgoing_edges(bpmn_elements)
    return convert_to_text_simple(bpmn_elements)


# Decodes a Base64 encoded string
def b64dec(b64_encoded: str):
    message = base64.b64decode(b64_encoded)
    return message.decode('ascii')


# Parses a BPMN di file, returns dictionary of BpmnElements and the start event's ID
def parse_bpmn_di(process: ET.Element):
    bpmn_elements = {}
    start_event_id = ''
    for child in process:
        if "id" not in child.attrib:
            continue

        child_id = child.attrib["id"]
        if "id" in child.attrib and "name" in child.attrib:
            if "startEvent" in child.tag:
                start_event_id = child_id
            outgoing_edges = get_edges(process, id=child.attrib["id"], edge_type="outgoing")
            incoming_edges = get_edges(process, id=child.attrib["id"], edge_type="incoming")

            bpmn_elements[child.attrib["id"]] = BpmnElement(uuid=child.attrib["id"], name=child.attrib["name"],
                                                            element_type=child.tag, incoming=set(incoming_edges),
                                                            outgoing=set(outgoing_edges))
        if "sequenceFlow" in child.tag and "name" not in child.attrib:
            outgoing_edges = get_edges(process, id=child.attrib["id"], edge_type="outgoing")
            incoming_edges = get_edges(process, id=child.attrib["id"], edge_type="incoming")
            bpmn_elements[child.attrib["id"]] = BpmnElement(uuid=child.attrib["id"], name='',
                                                            element_type=child.tag, incoming=set(incoming_edges),
                                                            outgoing=set(outgoing_edges))
    return bpmn_elements, start_event_id


# Adds the missing outgoing edges. This is needed if the depth first walk is to be used for converting the BPMN to text.
def add_missing_outgoing_edges(bpmn_elements):
    # Add the outgoing edges to all sequence flows
    expanded_outgoing_edges = {}
    for e in bpmn_elements:
        expanded_outgoing_edges[e] = []

    for uuid in bpmn_elements:
        element = bpmn_elements[uuid]
        for incoming in element.incoming:
            expanded_outgoing_edges[incoming].append(uuid)

    # Update the outgoing edges
    for uuid in bpmn_elements:
        element = bpmn_elements[uuid]
        for expanded_outgoing in expanded_outgoing_edges[uuid]:
            element.outgoing.add(expanded_outgoing)


# Iterative depth first algorithm for creating a text from a bpmn process
def convert_to_text_dfs(bpmn_elements, start_event_id):
    if start_event_id is None or start_event_id not in bpmn_elements:
        return "Invalid input!"

    path = []
    path_ids = []
    text = ""
    stack = [bpmn_elements[start_event_id]]
    while len(stack) != 0:
        element = stack.pop()
        if element.uuid not in path_ids:
            path_ids.append(element.uuid)
            path.append(element)
            if element.name != "":
                if "exclusiveGateway" in element.element_type:
                    text += "if " + element.name + " is "
                elif "sequenceFlow" in element.element_type:
                    text += element.name + " "
                else:
                    text += element.name + ". "

        for outgoing in element.outgoing:
            stack.append(bpmn_elements[outgoing])
    return text


# Simple implementation of converting a dictionary of BpmnElements to a text.
# Doesn't suffer from the disadvantages of the depth first walk implementation. It can handle loops.
def convert_to_text_simple(bpmn_elements):
    text = ""
    for key in bpmn_elements:
        if not bpmn_elements[key].name == "":
            text += bpmn_elements[key].name + ". "
    return text


# Convenience method for getting the incoming/outgoing edges
def get_edges(process, id, edge_type):
    if edge_type != "outgoing" and edge_type != "incoming":
        print("Invalid edge type!")
        return
    return [e.text for e in process.findall(f".//*[@id='{id}']/{NAMESPACE}{edge_type}")]


class BpmnElement(object):
    def __init__(self, uuid='', name='', element_type='', incoming=set(), outgoing=set()):
        self.uuid = uuid
        self.name = name
        self.element_type = element_type
        self.incoming = incoming
        self.outgoing = outgoing

    def __repr__(self):
        return f"id: {self.uuid}: {self.element_type}, {self.name}," \
               f" incoming: {', '.join(self.incoming)} outgoing: {', '.join(self.outgoing)}"
