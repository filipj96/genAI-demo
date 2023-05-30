export type ParsedAnswer = {
    parsedAnswer: string;
    followupQuestions: string[];
}

export function assistantAnswerParser(answer: string): ParsedAnswer {
    const followupQuestions: string[] = [];

    // Parse out all potential follow-up questions from the answer
    let parsedAnswer = answer.replace(/<<([^>>]+)>>/g, (match, content) => {
        followupQuestions.push(content);
        return "";
    })

    parsedAnswer = parsedAnswer.trim()

    return {
        parsedAnswer,
        followupQuestions
    }
}