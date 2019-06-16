#include "VM.h"
#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>

static int sp;       // 寄存器  栈指针: 指向栈中下一个最顶的基址
static int local;    // 寄存器  指向当前VM函数local的基址
static int argument; // 寄存器  指向当前VM函数argument段的基址
static int _this;    // 寄存器  指向当前this段(在堆中)的基址
static int that;     // 寄存器  指向当前that段(在堆中)的基址
static int ip;       // 寄存器  指向下一条要执行的指令
static int temp[7];  // 寄存器  存储临时值
/*
 *       RAM地址                 功能
 *          0~15            保留着,未使用
 *        16~155            VM程序的所有VM函数的静态变量
 *      256~2047            栈
 *    2048~16383            堆(用于存放对象和数组)
 **/

static short ram[266385];                       // 数据存储器
static vector<vector<string>> instructions_ram; // 指令存储器
static int staticCount;                         // 记录静态变量已经分配的数量
// 哈希表 ref : https://www.sczyh30.com/posts/C-C/cpp-stl-hashmap/
static unordered_map<string, int> staticVarNames;      // 记录静态变量在内存中的位置
static unordered_map<string, int> instruction_address; // 保存label和function指令在指令存储器中的地址
static vector<string> currentInstruction;              // 保存当前正在执行的指令
static string currentClassName;                        // 保存当前正在执行的指令所在的类的名字
static bool arriveEnd = false;                         // 标记是否到达程序结尾

void executeArithmetic(string const &command)
{
    // 执行算术指令
    if (command == "add")
    {
        ram[sp - 2] = ram[sp - 2] + ram[sp - 1];
        sp--;
    }
    else if (command == "sub")
    {
        ram[sp - 2] = ram[sp - 2] - ram[sp - 1];
        sp--;
    }
    else if (command == "neg")
    {
        ram[sp - 1] = -ram[sp - 1];
    }
    else if (command == "eq")
    {
        if (ram[sp - 2] == ram[sp - 1])
        {
            ram[sp - 2] = -1;
        }
        else
        {
            ram[sp - 2] = 0;
        }
        sp--;
    }
    else if (command == "gt")
    {
        if (ram[sp - 2] > ram[sp - 1])
        {
            ram[sp - 2] = -1;
        }
        else
        {
            ram[sp - 2] = 0;
        }
        sp--;
    }
    else if (command == "lt")
    {
        if (ram[sp - 2] < ram[sp - 1])
        {
            ram[sp - 2] = -1;
        }
        else
        {
            ram[sp - 2] = 0;
        }
        sp--;
    }
    else if (command == "and")
    {
        ram[sp - 2] = ram[sp - 2] & ram[sp - 1];
        sp--;
    }
    else if (command == "or")
    {
        ram[sp - 2] = ram[sp - 2] | ram[sp - 1];
        sp--;
    }
    else if (command == "not")
    {
        ram[sp - 1] = ~ram[sp - 1];
    }
}
void executePush(string const &segment, int index)
{
    // 执行push指令
    if (segment == "static")
    {
        string t;
        ostringstream iss(t); // 能够根据内容自动分配内存，并且其对内存的管理也是相当的到位
        iss << index;
        string staticVarName = currentClassName + "." + t;
        auto result = staticVarNames.find(staticVarName);
        if (result == staticVarNames.end())
        { // 未找到
            staticVarNames.insert({staticVarName, staticCount});
            staticCount++;
        }
        else
        { // 找到 获得偏移量
            int temp = ram[16 + result->second];
            ram[sp++] = temp;
        }
    }
    else if (segment == "argument")
    {
        ram[sp++] = ram[argument + index];
    }
    else if (segment == "local")
    {
        ram[sp++] = ram[local + index];
    }
    else if (segment == "constant")
    {
        ram[sp++] = index;
    }
    else if (segment == "this")
    {
        ram[sp++] = ram[_this + index];
    }
    else if (segment == "that")
    {
        ram[sp++] = ram[that + index];
    }
    else if (segment == "pointer")
    {
        if (index == 0)
        {
            ram[sp++] = _this;
        }
        else if (index == 1)
        {
            ram[sp++] = that;
        }
    }
    else if (segment == "temp")
    {
        ram[sp++] = temp[index];
    }
}

void executePop(string const &segment, int index)
{
    // 执行pop指令
    if (segment == "static")
    {
        string t;
        ostringstream iss(t); // 能够根据内容自动分配内存，并且其对内存的管理也是相当的到位
        iss << index;
        string staticVarName = currentClassName + "." + t;
        auto result = staticVarNames.find(staticVarName);
        if (result == staticVarNames.end())
        { // 未找到
            staticVarNames.insert({staticVarName, staticCount});
            staticCount++;
        }
        else
        { // 找到 获得偏移量
            int temp = ram[--sp];
            ram[16 + result->second] = temp;
        }
    }
    else if (segment == "argument")
    {
        ram[argument + index] = ram[--sp];
    }
    else if (segment == "local")
    {
        ram[local + index] = ram[--sp];
    }
    else if (segment == "this")
    {
        ram[_this + index] = ram[--sp];
    }
    else if (segment == "that")
    {
        ram[that + index] = ram[--sp];
    }
    else if (segment == "pointer")
    {
        if (index == 0)
        {
            _this = ram[--sp];
        }
        else if (index == 1)
        {
            that = ram[--sp];
        }
    }
    else if (segment == "temp")
    {
        temp[index] = ram[--sp];
    }
}
void executeLabel(string const &label)
{
    // 执行label指令
    instruction_address.insert({label, ip});
}
void executeGoto(string const &label)
{
    // 执行goto指令
    ip = instruction_address.find(label)->second;
}
void executeIf(string const &label)
{
    // 执行if-goto指令
    int temp = ram[--sp];
    if (temp == 0)
    {
        return;
    }
    ip = instruction_address.find(label)->second;
}
void executeCall(string const &functionName, int numArgs)
{
    // 执行call指令
    if (functionName == "IO.putchar")
    {
        putchar(ram[sp - 1]);
        return;
    }
    else if (functionName == "IO.getchar")
    {
        ram[sp++] = getchar();
        return;
    }
    /*
    ip
    local
    argument
    this
    that
    */
    ram[sp++] = ip;
    ram[sp++] = local;
    ram[sp++] = argument;
    ram[sp++] = _this;
    ram[sp++] = that;
    argument = sp - numArgs - 5;
    local = sp;
    ip = instruction_address.find(functionName)->second;
}
void executeReturn()
{
    // 执行return指令
    int temp = local;
    ip = ram[temp - 5];
    ram[argument] = ram[--sp]; // 重置调用的返回值
    sp = argument + 1;
    that = ram[temp - 1];
    _this = ram[temp = 2];
    argument = ram[temp - 3];
    local = ram[temp - 4];
}
void executeFunction(string const &functionName, int numLocals)
{
    // 执行function指令
    auto iter = functionName.cbegin();
    while (iter != functionName.cend())
    {
        if (*iter++ == '.')
        {
            break;
        }
        currentClassName = string(functionName.cbegin(), --iter);
        for (int i = 0; i < numLocals; i++)
        {
            ram[sp++] = 0;
        }
    }
}
void executeEnd()
{
    // 程序结束
}

void init()
{
    // cpu通电之后初始化ip
    ip = instruction_address.find("Sys.init")->second;
    sp = 50;
    local = sp;
    ram[local - 5] = instructions_ram.size() - 1;
}
void instructionFetch()
{
    // cpu取指令
    currentInstruction = instructions_ram[ip];
}
void execute()
{
    // cpu执行指令
    string command = currentInstruction[0];
    if (command == "add" || command == "sub" || command == "neg" ||
        command == "eq" || command == "gt" || command == "lt" ||
        command == "and" || command == "or" || command == "not")
    {
        executeArithmetic(currentInstruction[0]);
    }
    else if (command == "push")
    {
        executePush(currentInstruction[1], atoi(currentInstruction[2].c_str()));
    }
    else if (command == "pop")
    {
        executePop(currentInstruction[1], atoi(currentInstruction[2].c_str()));
    }
    else if (command == "label")
    {
        executeLabel(currentInstruction[1]);
    }
    else if (command == "goto")
    {
        executeGoto(currentInstruction[1]);
    }
    else if (command == "if-goto")
    {
        executeIf(currentInstruction[1]);
    }
    else if (command == "call")
    {
        executeCall(currentInstruction[1], atoi(currentInstruction[2].c_str()));
    }
    else if (command == "return")
    {
        executeReturn();
    }
    else if (command == "function")
    {
        executeFunction(currentInstruction[1], atoi(currentInstruction[2].c_str()));
    }
    else if (command == "end")
    {
        arriveEnd = true;
    }
}

void setKeyboardValue(short val)
{
    // 设置键盘指令
}
void loadProgram()
{
    // 载入程序到指令存储器中
}
void run()
{
    // CPU通电开始运行
    init();
    while (true)
    {
        instructionFetch();
        if (ip == 1)
        {
            int temp = 0;
        }
        ++ip;
        execute();
        if (arriveEnd == true)
        {
            break;
        }
    }
}