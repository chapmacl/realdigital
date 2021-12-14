import copy
import random
import os


# for debugging purposes
def generate_lists(number_of_lists: int):
    if not os.path.exists('files'):
        os.mkdir('files')
    for i in range(number_of_lists):
        new_list = []
        length = random.randint(5, 10)
        for j in range(length):
            new_list.append(random.randint(1, 20))
        new_list.sort()
        path = os.path.join('files', f'file_{i}.txt')
        with open(path, "w") as output:
            for number in new_list:
                output.write(str(number) + '\n')


'''
***FEEL FREE TO IGNORE THIS METHOD*** 

This method was loosely based on external merge sort, but doesn't quite work because the chunks were processed 
sequentially, and not in order of importance. For example:
    [1,1,1,1] and [1,2,2,3] 
would be sorted as: [1,1,1,2,1,2,3]. Still might be useful to see my original thought process, and the final list is 
"mostly" sorted, so this method got me about 90% of the way there.
'''


def combine_lists_wrong(files_dir: str, buffer: int, out_dir):
    # we need to use an external sort, since memory is our bottleneck
    count = 0
    file_names = [name for name in os.listdir(files_dir)]

    while True:
        output_list = []

        # using count, we can control the range for our chunks
        start = count * buffer
        end = (count + 1) * buffer
        for name in file_names:
            path = os.path.join(files_dir, name)
            with open(path, "r") as in_file:
                for i, line in enumerate(in_file):
                    if start <= i < end:
                        output_list.append(int(line))

                    # This short circuit makes our code slightly more efficient
                    elif i >= end:
                        break
                    # TODO No sense in iterating a file with lines < start. We should remove it from file_names...

        # if temp_list is empty, we know we're done, so we can break out
        if not output_list:
            break

        # For this example, output_list is guaranteed to be small so no need for fancy merging algorithms.
        # As a matter of fact, if the sub-lists are already sorted, then worst case will never happen anyways...
        output_list.sort()

        with open(out_dir, "a") as out_file:
            for number in output_list:
                out_file.write(str(number) + '\n')

        count += 1


'''
This method works a lot smarter instead of harder. Important detail is that the files are already sorted, so instead
of performing a merge sort we can just sort the numbers in a kind of "in-place" but not really in-place way. We know 
that every file is sorted, so we just need to compare the elements of each file in order of index and insert the min
to our output list each time. Luckily, we are able to iterate through files by line, instead of loading them entirely 
in memory. This strategy also has the benefit of not needing to create additional temporary files. 
'''


def combine_lists(files_dir: str, out_dir: str):
    file_names = os.listdir(files_dir)
    wrappers = []
    candidates = []
    for name in file_names:
        path = os.path.join(files_dir, name)
        f = open(path, "r")
        wrappers.append(f)
        # We assume that no files are empty, otherwise this would cause problems for us.
        candidates.append(int(f.readline()))

    # Not necessary, but also not a bad idea...
    if os.path.exists(out_dir):
        os.remove(out_dir)

    while candidates:
        min_candidate = min(candidates)
        min_index = candidates.index(min_candidate)

        # there is probably a better way to do this than calling open() each time...
        with open(out_dir, "a") as out_file:
            out_file.write(str(min_candidate) + '\n')

        new_candidate = wrappers[min_index].readline()
        # At end-of-file, readline() returns empty string. Should this happen, we need to remove it.
        # Eventually, candidates will be empty, and then our loop exits
        if new_candidate == '':
            # Don't forget to close the file!
            wrappers[min_index].close()
            del wrappers[min_index]
            del candidates[min_index]
        else:
            candidates[min_index] = int(new_candidate)


if __name__ == '__main__':
    generate_lists(10)
    combine_lists('files', 'output.txt')

    # Check for correctness

    output = []
    with open('output.txt', 'r') as f:
        output.extend(f.read().splitlines())

    output = [int(x) for x in output]
    test_list = copy.deepcopy(output)
    test_list.sort()
    print(output == test_list)
