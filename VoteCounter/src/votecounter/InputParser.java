/**
 * InputParser.java: parses XML input
 * Copyright (C) 2013 Shardul C.
 *
 * This file is part of VoteCounter.
 *
 * VoteCounter is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * VoteCounter is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with VoteCounter.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Bugs, tips, suggestions, requests to <shardul.chiplunkar@gmail.com>
 * or <mjuvekar7@gmail.com>.
 */

package votecounter;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import org.jdom2.*;
import org.jdom2.input.*;

/**
 * XML input parser for {@link VoteCounter}.
 *
 * This class provides methods for parsing an XML input file and converting the
 * data into a format usable by the vote counting application. Currently, all
 * data is being entered by hand (hard-coded): the program would be more
 * flexible and useful for many others if the data could be in a predefined
 * format, such as XML. We are working towards making XML files the primary mode
 * of input to the program.
 *
 * @author shardul
 */
public class InputParser {

    private List<String> groups;
    private List<String> genericPosts;
    private String[][] genericNominees;
    private List<String> nonGenericPosts;
    private String[][][] nonGenericNominees;

    /**
     * Parse the XML input file and get groups, posts, and nominees.
     *
     * The {@code parse} method parses the document using
     * {@link org.jdom2.input.SAXBuilder} which builds a pseudo-tree structure
     * representing the XML file. The method then traverses each element and
     * builds a representation of the data that makes sense to the vote-counting
     * program; that is, it organizes the data into posts and groups as
     * specified in the input file.
     *
     * The behavior of the {@code parse} method is unspecified if the XML file
     * is not structured as it expects it to be. This can happen even if the
     * syntax is all right, because of mispelings or order elements of incorrect
     * the. A format specifier file is coming soon.
     *
     * @param is an {@link java.io.InputStream} for the XML input file
     * @throws JDOMException if XML structure/syntax is incorrect
     * @throws IOException if error accessing file
     */
    public void parse(java.io.InputStream is) throws JDOMException, IOException {
        Element root = ((new SAXBuilder()).build(is)).getRootElement();
        int listSize;

        List<Element> groupList = root.getChild("groups").getChildren();
        String[] groupArray = new String[groupList.size()];
        for (int i = 0; i < groupList.size(); i++) {
            groupArray[i] = groupList.get(i).getText();
        }
        groups = Arrays.asList(groupArray);

        List<Element> genericPostList = root.getChild("posts").getChild("generic").getChildren();
        listSize = genericPostList.size();
        List<Element> nominees;
        String[] genericPostArray = new String[listSize];
        genericNominees = new String[listSize][];
        for (int i = 0; i < listSize; i++) {
            genericPostArray[i] = genericPostList.get(i).getAttributeValue("name");
            nominees = genericPostList.get(i).getChildren();
            genericNominees[i] = new String[nominees.size()];
            for (int j = 0; j < nominees.size(); j++) {
                genericNominees[i][j] = nominees.get(j).getText();
            }
        }
        genericPosts = Arrays.asList(genericPostArray);

        // you better document this stuff NOW
        // or else it'll work, but no-one will know HOW

        List<Element> nonGenericPostList = root.getChild("posts").getChild("nongeneric").getChildren();
        listSize = nonGenericPostList.size();
        List<Element> competingGroups;
        List<Element> groupNominees;
        String[] nonGenericPostArray = new String[listSize];
        nonGenericNominees = new String[listSize][][];
        for (int i = 0; i < listSize; i++) {
            nonGenericPostArray[i] = nonGenericPostList.get(i).getAttributeValue("name");
            competingGroups = nonGenericPostList.get(i).getChildren();
            nonGenericNominees[i] = new String[groups.size()][];
            int group;
            for (int j = 0; j < competingGroups.size(); j++) {
                group = groups.indexOf(competingGroups.get(j).getAttribute("name").getValue());
                groupNominees = competingGroups.get(j).getChildren();
                nonGenericNominees[i][group] = new String[groupNominees.size()];
                for (int k = 0; k < groupNominees.size(); k++) {
                    nonGenericNominees[i][group][k] = groupNominees.get(k).getText();
                }
            }
        }
        nonGenericPosts = Arrays.asList(nonGenericPostArray);
    }

    /**
     * Get list of nominee groups.
     *
     * @return list of nominee groups
     */
    public List<String> getGroups() {
        return groups;
    }

    /**
     * Get array of nominees in generic (non-group) categories.
     *
     * The two dimensional array is of the form {@code String[posts][nominees for each
     * post]}.
     *
     * @return array of generic nominees
     */
    public String[][] getGenericNominees() {
        return genericNominees;
    }

    /**
     * Get array of nominees in non-generic (group-wise) categories.
     *
     * The three dimensional array is of the form
     * {@code String[posts][contesting groups][nominees for each group in each post]}.
     *
     * @return array of non-generic nominees
     */
    public String[][][] getNonGenericNominees() {
        return nonGenericNominees;
    }

    /**
     * Get list of generic (non-group) posts.
     *
     * @return list of generic posts
     */
    public List<String> getGenericPosts() {
        return genericPosts;
    }

    /**
     * Get list of non-generic (group-wise) posts.
     *
     * @return list of non-generic posts
     */
    public List<String> getNonGenericPosts() {
        return nonGenericPosts;
    }
}
