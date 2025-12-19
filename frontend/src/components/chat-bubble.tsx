import { Card, CardBody, Avatar } from "@nextui-org/react";

interface ChatBubbleProps {
  role: "user" | "ai";
  content: string;
}

export default function ChatBubble({ role, content }: ChatBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={`flex w-full gap-2 mb-4 ${isUser ? "justify-end" : "justify-start"}`}>
      {/* AI Avatar (Only show on left) */}
      {!isUser && (
        <Avatar 
          src="https://api.dicebear.com/9.x/bottts-neutral/svg?seed=DocuBot" 
          size="sm"
          isBordered 
        />
      )}

      <Card className={`max-w-[80%] ${isUser ? "bg-primary text-white" : "bg-default-100"}`}>
        <CardBody className="px-4 py-3 text-sm">
          {content}
        </CardBody>
      </Card>

      {/* User Avatar (Only show on right) */}
      {isUser && (
        <Avatar 
          src="https://i.pravatar.cc/150?u=a042581f4e29026704d" 
          size="sm" 
          isBordered
          color="primary"
        />
      )}
    </div>
  );
}