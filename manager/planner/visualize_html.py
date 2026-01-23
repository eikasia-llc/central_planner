#!/usr/bin/env python3
import sys
import os
import json
import webbrowser

# Setup path to find 'language' module
current_file_path = os.path.abspath(__file__)
planner_dir = os.path.dirname(current_file_path)
manager_dir = os.path.dirname(planner_dir)
root_dir = os.path.dirname(manager_dir)
language_dir = os.path.join(root_dir, 'language')

if language_dir not in sys.path:
    sys.path.append(language_dir)

try:
    from md_parser import MarkdownParser
except ImportError as e:
    print(f"Error: Could not import md_parser from {language_dir}. {e}")
    sys.exit(1)

# HTML Template with D3.js
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Master Plan Visualization</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; overflow: hidden; background: #f8f9fa; }
    #container { width: 100vw; height: 100vh; display: flex; }
    #viz { flex-grow: 1; height: 100%; position: relative; }
    #sidebar { width: 400px; height: 100vh; background: white; border-left: 1px solid #ddd; padding: 20px; box-sizing: border-box; overflow-y: auto; display: none; box-shadow: -2px 0 5px rgba(0,0,0,0.05); z-index: 10; transform: translateX(0); transition: transform 0.3s ease; }
    #sidebar.hidden { transform: translateX(100%); display: block; }
    
    .node circle { fill: #fff; stroke: steelblue; stroke-width: 2px; cursor: pointer; transition: all 0.3s; }
    .node circle:hover { stroke-width: 4px; }
    .node text { font: 12px sans-serif; cursor: pointer; }
    
    .link { fill: none; stroke: #ccc; stroke-width: 1.5px; transition: all 0.5s; stroke-opacity: 0.6; }

    /* Metadata Colors */
    .status-done { stroke: #2ecc71 !important; fill: #e8f8f5 !important; }
    .status-active { stroke: #3498db !important; fill: #ebf5fb !important; }
    .status-todo { stroke: #bdc3c7 !important; fill: #fbfcfc !important; }
    .status-blocked { stroke: #e74c3c !important; fill: #fdedec !important; }
    
    h2 { margin-top: 0; font-size: 1.5em; color: #2c3e50; }
    .meta-tag { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; margin-right: 5px; margin-bottom: 5px; color: white; font-weight: 500;}
    
    .tag-todo { background: #95a5a6; }
    .tag-active { background: #3498db; }
    .tag-done { background: #2ecc71; }
    .tag-blocked { background: #e74c3c; }
    .tag-default { background: #7f8c8d; }

    pre { background: #f4f6f7; padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 0.9em; white-space: pre-wrap; }
    .content-block { line-height: 1.6; color: #34495e; font-size: 0.95em; }

    .control-panel { position: absolute; top: 20px; left: 20px; background: rgba(255, 255, 255, 0.9); padding: 10px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    button { background: #3498db; color: white; border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; font-size: 13px; }
    button:hover { background: #2980b9; }

    /* Markdown styling specifics */
    .content-block h1, .content-block h2, .content-block h3 { margin-top: 1.2em; color: #2c3e50; }
    .content-block code { background: #eee; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
  </style>
</head>
<body>

<div id="container">
  <div id="viz">
    <svg width="100%" height="100%"></svg>
    <div class="control-panel">
        <button onclick="expandAll()">Expand All</button>
        <button onclick="collapseAll()">Collapse All</button>
        <button onclick="resetZoom()">Reset Zoom</button>
    </div>
  </div>
  <div id="sidebar">
    <div id="details">
        <h2 style="color: #bbb;">Select a node...</h2>
    </div>
  </div>
</div>

<script>
const data = __DATA_PLACEHOLDER__;

const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("svg")
    .attr("width", width)
    .attr("height", height);

const g = svg.append("g");

const zoom = d3.zoom()
    .scaleExtent([0.1, 4])
    .on("zoom", (event) => g.attr("transform", event.transform));

svg.call(zoom);

let i = 0;
let duration = 500;
let root;

// Tree Layout
const tree = d3.tree().nodeSize([30, 250]); // Height, Width between levels

root = d3.hierarchy(data, d => d.children);
root.x0 = height / 2;
root.y0 = 0;

// Collapse after level 2 by default
root.children.forEach(collapse);

update(root);

function collapse(d) {
  if(d.children) {
    d._children = d.children;
    d.children.forEach(collapse);
    d.children = null;
  }
}

function expand(d) {
    if (d._children) {
        d.children = d._children;
        d.children.forEach(expand); // Recursive? maybe just one level
        d._children = null;
    }
}

function expandAll() {
    // Helper to recursively expand
    function recurse(d) {
        if (d._children) {
            d.children = d._children;
            d._children = null;
        }
        if (d.children) d.children.forEach(recurse);
    }
    recurse(root);
    update(root);
}

function collapseAll() {
    function recurse(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        }
        if (d._children) d._children.forEach(recurse);
    }
    // Don't collapse root's direct children so we see something
    if (root.children) root.children.forEach(recurse);
    update(root);
}

function resetZoom() {
    svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity.translate(100, height/2).scale(1));
}

function update(source) {
  const treeData = tree(root);

  // Compute the new tree layout.
  const nodes = treeData.descendants();
  const links = treeData.links();

  // Normalize for fixed-depth.
  nodes.forEach(d => { d.y = d.depth * 250; });

  // ****************** Nodes section ***************************

  // Update the nodes...
  const node = g.selectAll('g.node')
      .data(nodes, d => d.id || (d.id = ++i));

  // Enter any new modes at the parent's previous position.
  const nodeEnter = node.enter().append('g')
      .attr('class', 'node')
      .attr("transform", d => "translate(" + source.y0 + "," + source.x0 + ")")
      .on('click', click)
      .on('mouseover', function() { d3.select(this).select("text").attr("font-weight", "bold"); })
      .on('mouseout', function() { d3.select(this).select("text").attr("font-weight", "normal"); });

  nodeEnter.append('circle')
      .attr('r', 1e-6)
      .attr('class', d => {
          const status = d.data.metadata && d.data.metadata.status ? d.data.metadata.status : 'default';
          return `status-${status}`;
      });

  nodeEnter.append('text')
      .attr("dy", ".35em")
      .attr("x", d => d.children || d._children ? -13 : 13)
      .attr("text-anchor", d => d.children || d._children ? "end" : "start")
      .text(d => {
          let title = d.data.title;
          return title.length > 25 ? title.substring(0, 25) + '...' : title;
      })
      .style('fill-opacity', 1e-6);

  // UPDATE
  const nodeUpdate = nodeEnter.merge(node);

  // Transition to the proper position for the node
  nodeUpdate.transition()
    .duration(duration)
    .attr("transform", d => "translate(" + d.y + "," + d.x + ")");

  // Update the circle attribute to match new data
  nodeUpdate.select('circle')
    .attr('r', 8)
    .style("fill", d => d._children ? "#fff" : "") // White if collapsed
    .attr('class', d => {
          const status = d.data.metadata && d.data.metadata.status ? d.data.metadata.status : 'default';
          return `status-${status}`;
      });

  nodeUpdate.select('text')
    .style("fill-opacity", 1);

  // Exit any old nodes.
  const nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", d => "translate(" + source.y + "," + source.x + ")") # Target parent position? No, source usually
      .remove();

  nodeExit.select('circle')
    .attr('r', 1e-6);

  nodeExit.select('text')
    .style('fill-opacity', 1e-6);

  // ****************** Links section ***************************

  // Update the links...
  const link = g.selectAll('path.link')
      .data(links, d => d.target.id);

  // Enter any new links at the parent's previous position.
  const linkEnter = link.enter().insert('path', "g")
      .attr("class", "link")
      .attr('d', d => {
        const o = {x: source.x0, y: source.y0}
        return diagonal(o, o)
      });

  // UPDATE
  const linkUpdate = linkEnter.merge(link);

  // Transition back to the parent element position
  linkUpdate.transition()
      .duration(duration)
      .attr('d', d => diagonal(d.source, d.target));

  // Remove any exiting links
  const linkExit = link.exit().transition()
      .duration(duration)
      .attr('d', d => {
        const o = {x: source.x, y: source.y}
        return diagonal(o, o)
      })
      .remove();

  // Store the old positions for transition.
  nodes.forEach(d => {
    d.x0 = d.x;
    d.y0 = d.y;
  });

  // Creates a curved (diagonal) path from parent to the child nodes
  function diagonal(s, d) {
    path = `M ${s.y} ${s.x}
            C ${(s.y + d.y) / 2} ${s.x},
              ${(s.y + d.y) / 2} ${d.x},
              ${d.y} ${d.x}`
    return path
  }

  // Toggle children on click or show details
  function click(event, d) {
    // If clicked on circle (target is circle), toggle collapse
    // If clicked on text, show details
    // But simplified: Click toggles collapse AND shows details
    showDetails(d.data);
    
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
    update(d);
  }
}

function showDetails(data) {
    const sidebar = document.getElementById('sidebar');
    const container = document.getElementById('details');
    sidebar.style.display = 'block';

    const status = data.metadata.status || 'todo';
    const cleanStatus = status.replace('-', '');
    
    let metaHtml = '';
    for (const [key, value] of Object.entries(data.metadata)) {
        if (key === 'status') continue;
        metaHtml += `<div><strong>${key}:</strong> ${JSON.stringify(value)}</div>`;
    }

    // Convert markdown (simple) to html
    // Just escaping mostly or basic replacement since we don't have a parser here
    // For simplicity, we just use pre-wrap
    
    container.innerHTML = `
        <span class="meta-tag tag-${status}">${status.toUpperCase()}</span>
        <h2>${data.title}</h2>
        <div style="margin-bottom: 20px; font-size: 0.9em; color: #7f8c8d;">
            ${metaHtml}
        </div>
        <hr style="border: 0; border-top: 1px solid #eee;"/>
        <div class="content-block">
            <pre style="background:none; padding:0;">${data.content || "No content."}</pre>
        </div>
    `;
}

// Initial center
d3.select("svg").call(zoom.transform, d3.zoomIdentity.translate(100, height/2));

</script>
</body>
</html>
"""

def node_to_dict(node):
    # Flatten children to simplify D3 digestion
    return {
        "title": node.title,
        "metadata": node.metadata,
        "content": node.content,
        "children": [node_to_dict(child) for child in node.children]
    }

def main():
    target_file = os.path.join(planner_dir, "MASTER_PLAN.md")
    if not os.path.exists(target_file):
        print("MASTER_PLAN.md not found")
        sys.exit(1)

    print(f"Parsing {target_file}...")
    parser = MarkdownParser()
    root_node = parser.parse_file(target_file)
    
    # Check if root has children, if not something is wrong or empty
    if not root_node.children and not root_node.content and root_node.title == "Root":
        # Sometimes root is artificial container, check first level
        pass

    # Convert to JSON dict
    # If root is artificial "Root", we might want to skip it if it has only one child which is real document title
    # But safe to keep it.
    
    # We prefer the visual root to be the Doc Title
    if root_node.title == "Root" and len(root_node.children) == 1:
        data = node_to_dict(root_node.children[0])
    else:
        data = node_to_dict(root_node)
        
    json_data = json.dumps(data)
    
    # Inject into HTML
    html_content = HTML_TEMPLATE.replace("__DATA_PLACEHOLDER__", json_data)
    
    output_path = os.path.join(planner_dir, "master_plan_interactive.html")
    with open(output_path, 'w') as f:
        f.write(html_content)
        
    print(f"Visualization saved to: {output_path}")
    
    # Try to open
    try:
        webbrowser.open('file://' + os.path.abspath(output_path))
    except Exception as e:
        print(f"Could not open browser: {e}")

if __name__ == "__main__":
    main()
