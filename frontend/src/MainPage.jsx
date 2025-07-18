import React from "react";
import axios from "axios";
import { Input, Card, Space, Button, List } from "antd";
import "./mainpage.css";

const MainPage = () => {
	const [input, setInput] = React.useState("");
	const [output, setOutput] = React.useState([]);

	const scrollToItem = (itemId) => {
		console.log(itemId);
		const element = document.getElementById(itemId);

		if (element) {
			element.scrollIntoView({ behavior: "smooth" });
		}
	};

	const handleSubmit = async () => {
		console.log(input);
		const humanInput = "You: " + input;
		let newOutput = [...output, humanInput];
		setOutput(newOutput);
		const response = await axios.post("http://127.0.0.1:5000/run_agent", {
			input,
		});
		console.log(response.data);
		const aiAgentResponse = "AI Agent: " + response.data.response;
		newOutput = [...newOutput, aiAgentResponse];
		setOutput(newOutput);
		scrollToItem("outputvalue" + (newOutput.length - 1));
	};

	return (
		<div className="Main-Page">
			<Space.Compact className="Input">
				<Input
					placeholder="Enter your prompt here to do a Devops Task"
					value={input}
					onChange={(e) => setInput(e.target.value)}
				/>
				<Button
					type="primary"
					className="Button"
					onClick={handleSubmit}
				>
					Submit
				</Button>
			</Space.Compact>
			<Card title="Generating Output" className="Output">
				<List>
					{" "}
					{output.map((item, index) => (
						<List.Item key={index} id={"outputvalue" + index}>
							{item}
						</List.Item>
					))}
				</List>
			</Card>
		</div>
	);
};

export default MainPage;
