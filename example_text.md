# Example text for demonstration purposes

## AWS Community Dataset

### Chat
What are we talking about today at AWS meetup in Haarlem?

### Prompting with context
https://www.meetup.com/awsugnl/events/301382265/

Details
Meetup agenda
Generative AI has already gotten widespread acceptance in the world. AWS is also following this tends by their GenAI service, “Bedrock” as you see. To use GenAI. To consider using Bedrock, we will be minding that which AI model would be appropriate for the purpose, which AI model is precise about Token size, and which AI model is the best for the purpose about the cost. which model has strong for “prompting”, or so. This meetup will give attendees some hints for the above.

Date:
3rd July, 18:00 - 21:00 (Doors open at 17:30)

TimeTable:
18:00 - Doors open
19:00 - Session 1
19:30 - Session 2
20:00 - Session 3
20:30 - After hours
21:00 - Close

Place:
Koepelplein 1,
Cupolaxs Studio (https://www.locaties.nl/ruimte/studio-29759)

2031WL Haarlem
https://www.cupolaxs.nl/

Speaker:

Jettro Coenraide - Gen AI needs high-quality and performant search
Rakshaki Krishnamurthy - Adapting to Gen AI in retail: Key considerations to lay successful foundations
Gunnar Grosch - Enhance your app development with generative AI developer tools
Talks:

Jettro Coenraide
Large language models become more powerful every day. Each release adds more features, such as working with agents, pictures, code generation, and functions. One thing that will remain important is having access to knowledge and recent time-driven data. A now well-known pattern to overcome this problem is RAG or Retrieval Augmented Generation.This talk teaches you about the required components for a RAG-based system. An essential part is a search component, the retriever. For the retriever, you learn about Amazon OpenSearch Service’s capabilities. Together, we explore vector, lexical, and hybrid search. For the large language model to generate answers, and the embeddings, we use OpenAI. The demo application uses Rag4p, a basic RAG system perfectly suited for learning the different RAG components.
Rakshaki Krishnamurthy:
Who moved my cheese? Adapting to GenAI in Retail: The impact of GenAI in retail & key considerations for business leaders & engineering managers to evaluate in their GenAI transformation journey. In this session Rakshaki will share about the Gen AI opportunity in Europe, how’s Amazon adapting to Gen AI, how could you as an AWS customer adapt. She will draw upon her experiences from the ground on key success factors in getting business value from Gen AI
Gunnar Grosch
Generative AI can transform how developers and organizations build and manage applications. It streamlines the entire software development lifecycle — from planning to deployment — saving time and fostering creativity. In this session, we'll look at how generative AI developer tools can help developer focus on meaningful work that drives impact for their customers. We will also prototype a serverless generative AI application leveraging Amazon Bedrock from concept to a fully featured application using Amazon Q Developer in the IDE.
Note:
We will serve pizza and soft drinks.

Parking
Use Parkbee

#### Other questions
- What is the address of the venue?
- What time does the event start?
- Who are the speakers?

### Retrieving context

Link to the site for the content
https://dev.to/aws-builders

#### Questions
- What can you tell about combining streaming data with events?
- Who wrote about combining streaming data with events?
- What did Jimmy Dahlqvist write about?

### Using the right splitter and strategy
Every time I get the chance, I like to write articles that are geared towards enabling you make your cloud infrastructure on AWS and other cloud platforms more secure. In today’s edition of writing about AWS services, we will be learning about NAT Gateways, what they are, how they work and how they enhance our cloud infrastructure. From NAT gateways we will finish it off by talking about VPC endpoints. Allons-y (FYI: that’s “let’s go” in French 😉)NAT GatewaysFirst and foremost, NAT stands for Network Address Translation. Let’s look at what NAT really is before moving on to NAT gateways proper. Network Address Translation is a process in which private IP addresses used on a network (usually a local area network) are translated into public IP addresses that can be used to access the internet.To understand how NAT gateways work, we are going to use the example of a two-tier architecture with a web tier deployed on EC2 instance in a public subnet (a public subnet is a subnet that has a route to an Internet gateway on the route table associated with it) and an application tier deployed on EC2 instances in a private subnet ( a private subnet has no route to an internet gateway on its route table). With this architecture, the EC2 instances that make up the application tier are unable to access the internet because they the subnet in which they reside has no route to an IGW on its route table. How will the instances go about performing tasks like downloading update patches from the internet? The answer lies in using NAT gateways. For the application tier to have access to the internet, we need to provision a NAT gateway in the public subnet housing our web tier.When an instance in the application tier wants to connect to the internet, it sends a request which carries information such as the IP address of the instance and the destination of the request to the NAT gateway in the public subnet. The NAT gateway then translates the private IP address of the instance to a public elastic IP address in its address pool and uses it to forward the request to the internet via the internet gateway. One important thing to note about NAT gateways is that, they won’t accept or allow any inbound communication initiated from the internet as it only allows outbound traffic originating from your VPC. This can significantly improve the security posture of your infrastructure.NAT gateways are managed by AWS. To create a NAT gateway, all you have to do is specify the subnet it will reside in and then associate an Elastic IP address (EIP). AWS handles every other configuration for you.VPC EndpointsVPC endpoints allow private access to an array of AWS services using the internal AWS network instead of having to go through the internet using public DNS endpoints. These endpoints enable you to connect to supported services without having to configure an IGW (Internet Gateway), NAT Gateway, a VPN, or a Direct Connect (DX) connection.There are two types of VPC endpoints available on AWS. They are the Interface Endpoints and Gateway EndpointsInterface Endpoints— They are fundamentally Elastic Network Interfaces (ENI) placed in a subnet where they act as a target for any traffic that is being sent to a supported service. To be able to connect to an interface endpoint to access a supported service, you use PrivateLink. PrivateLink provides a secure and private connection between VPCs, AWS services and on-premises applications through the internal AWS network.To see the suite of services that can be accessed via interface endpoints, check out thisAWS documentation.Gateway Endpoints— They are targets within your route table that enable you to access supported services thereby keeping traffic within the AWS network. At the time of writing, the only services supported by gateway endpoints are: S3 and DynamoDB. Be sure to check the appropriate AWS documentation for any addition to the list of services. One last thing to keep in mind about gateway endpoints is that they only work with IPv4ConclusionSome say the mark of a good dancer is to know when to bow out of the stage. With that, we have officially reached the end of this article about VPC endpoints and NAT gateways. I will like to implore you to keep learning and getting better at using tools such as these for you don’t know when they will come in handy. That could be sooner rather than later. Thank you for riding with me to the very end. Best of luck in all your endeavors.




## Txt for splitter tutorial
It all started with Halloween. I wanted something special for the kids walking past my house. I created a talking skeleton, just like the Pirates of the Caribbean. I want the kids to have a safe conversation with the pirate, which was challenging for some details.  
  
In this talk, we will guide you through the interactive steps of creating the talking head. We'll delve into the interface with a Large Language Model, the implementation of guard rules, and the intriguing problem of a pirate conversing within these rules. To kickstart the conversation, we'll connect the program to a motion detector, allowing the pirate to interact with kids in their native language-a, a truly multi-lingual experience. 
 
Along the way, we will focus on problems like response time and content moderation, which can be quite difficult when the skeleton itself is already moderated. 
Our goal is to inspire more creatives to discover the joy of programming and apply their skills to a wide range of educational and entertainment projects. The talking skeleton is just one example of how programming can create engaging and interactive experiences. 
 
Technologies used: 


Open AI: Large Language Model, Chat, speech-to-text 
ElevenLabs: tekst-to-speech the pirate way 
Python: Glue between the different components 
Vue/Typescript: A frontend application to alternatively interact with the animatronic 
 
Guest appearance: Benno the Pirate! 
