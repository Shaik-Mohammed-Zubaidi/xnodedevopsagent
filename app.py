from flask import Flask, request, jsonify
from flask_cors import CORS

from agent5 import ReActAgent
from langchain_community.tools.tavily_search import TavilySearchResults
from tools import kubernetes_tool, docker_tool, save_to_file, terraform_tool

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# ✅ Initialize agent
agent = ReActAgent()

# ✅ Add tools dynamically
tool = TavilySearchResults(max_results=2)
agent.add_tool(tool)
agent.add_tool(save_to_file)
agent.add_tool(docker_tool)
agent.add_tool(kubernetes_tool)
agent.add_tool(terraform_tool)

# ✅ Build the graph with memory persistence
agent.build()

# # ✅ Run the agent
# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         break

#     agent.run(user_input)

@app.route("/run_agent", methods=["POST"])
def run_agent():
    try:
        data = request.json
        user_input = data.get("input", "")

        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        response = agent.run(user_input)
        return jsonify({"response": response})

    except Exception as e:
        console.log(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
